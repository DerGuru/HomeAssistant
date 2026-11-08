## Title
Homeassistant_sky_connect setup reads ZHA's zigbee.db even though the ZBT-1 is not used for Zigbee (can collide with ZHA startup: "database is locked")

## The problem
Setting up the `homeassistant_sky_connect` entry of a ZBT-1 makes Home Assistant
open ZHA's `zigbee.db` and read its last network backup, even though the ZBT-1
is not used for Zigbee and the Multiprotocol add-on is not installed or not used.
This is unnecessary work on a database that belongs to a different integration
and a different radio. In my case it coincided with ZHA's own startup right after updating to 2026.11.0, which then failed with `sqlite3.OperationalError: database is locked`.

The failing call in ZHA is a schema migration (`zigpy.appdb.PersistingListener._run_migrations`
-> `executescript`), executed in ZHA's own `async_setup_entry` ->
`radio_mgr.create_zigpy_app(connect=False)`. ZHA's config entry then stays in
`setup_error` and is not retried, so the whole Zigbee network is offline until
the entry is reloaded manually (`homeassistant.reload_config_entry`). A manual
reload succeeded right away, including the migration.

I could only observe this once and cannot reproduce it, since the migration was only done once. The main point of this issue is the design problem below; the lock is the visible consequence.

I have two radios, and each is used by exactly one integration:

| Stick | Firmware | Used by |
|---|---|---|
| Home Assistant Connect ZBT-1 | OpenThread RCP (`spinel`, `multiprotocol: false`) | OpenThread Border Router app (Thread only) |
| Home Assistant Connect ZBT-2 | EZSP 7.5.1.0 | ZHA (`radio_type: ezsp`) |

Zigbee is not configured on the ZBT-1 at all. The `homeassistant_sky_connect`
entry of the ZBT-1 nevertheless takes a long time to set up
(`config_entry_setup` ~57.5 s vs. ~11.9 s for the ZBT-2 entry).

### Code path (read from the 2026.11.0 sources)
1. `homeassistant_sky_connect.async_setup_entry` calls
   `multi_pan_addon_using_device(hass, device_path)`.
2. On Supervisor installs, `multi_pan_addon_using_device` first calls
   `get_multiprotocol_addon_manager(hass)` and only afterwards checks whether the
   add-on is running and uses this device. The manager is created even if the
   add-on is not installed.
3. `MultiprotocolAddonManager.async_setup` calls `async_process_integration_platforms(...,
   "silabs_multiprotocol", ..., wait_for_platforms=True)`.
4. `_register_multipan_platform` then calls, unconditionally,
   `platform.async_get_channel(hass)` and `platform.async_using_multipan(hass)`.
   The channel is only used if `using_multipan` is true (`if self._channel is not
   None or not using_multipan: return`).
5. ZHA's `async_get_channel` (`zha/silabs_multiprotocol.py`) calls
   `api.async_get_network_settings`. If the ZHA gateway is not running yet, this
   falls back to `async_get_last_network_settings`, which does
   `radio_mgr.create_zigpy_app(connect=False)` and reads
   `app.backups.most_recent_backup()`. That opens `zigbee.db` and runs the zigpy
   DB migrations.

So on a Supervisor install, the ZBT-1 setup opens ZHA's database even when the
add-on is not used, only to read a channel it then discards. `async_using_multipan`
in ZHA is cheap (it only compares the radio path with the add-on URL) and could
be evaluated first.

I suspect a race between this second zigpy app and ZHA's own startup, but
the traceback only shows ZHA's side, so this part is inferred.

## What version of Home Assistant Core has the issue?
2026.11.0 (zha 2.4.2, zigpy 2.4.1, bellows 1.2.1, zha-quirks 2.4.1)

## What was the last working version of Home Assistant Core?
2026.10.x (zha 2.3.1, older zigpy). ZHA loaded fine at every earlier start.
It is unclear to me why a schema migration (`_run_migrations`) ran at this
start; the zigpy 2.4.0/2.4.1 release notes do not mention a DB migration.

## What type of installation are you running?
Home Assistant OS 18.4 on Home Assistant Green (Supervisor 2026.10.5, aarch64, Python 3.14.10)

## Integration causing the issue
Zigbee Home Automation (ZHA)
(Possibly also `homeassistant_sky_connect` / `homeassistant_hardware`)

## Link to integration documentation on our website
https://www.home-assistant.io/integrations/zha/

## Diagnostics information
Not attached (ZHA was in `setup_error` when the problem was noticed).

## Example YAML snippet
Not applicable.

## Anything in the logs that might be useful for us?
```txt
Logger: homeassistant.config_entries
Source: config_entries.py:1023
First occurred: 09:46:52 (1 occurrence)

Error setting up entry Home Assistant Connect ZBT-2 for zha
Traceback (most recent call last):
  File ".../homeassistant/config_entries.py", line 1023, in __async_setup_with_context
    setup_result = await component.async_setup_entry(hass, self)
  File ".../homeassistant/components/zha/__init__.py", line 188, in async_setup_entry
    async with radio_mgr.create_zigpy_app(connect=False, device_resolver=DEVICE_REGISTRY.resolve) as app:
  File ".../homeassistant/components/zha/radio_manager.py", line 216, in create_zigpy_app
    app = await self.radio_type.controller.new(...)
  File ".../zigpy/application.py", line 361, in new
    await app._load_db()
  File ".../zigpy/application.py", line 168, in _load_db
    self._dblistener = await zigpy.appdb.PersistingListener.new(database_file, self)
  File ".../zigpy/appdb.py", line 212, in new
    await listener.initialize_tables()
  File ".../zigpy/appdb.py", line 197, in initialize_tables
    await self._run_migrations()
  File ".../zigpy/appdb.py", line 1544, in _run_migrations
    await self.executescript(zigpy.appdb_schemas.SCHEMAS[to_db_version])
  File ".../zigpy/appdb.py", line 361, in executescript
    await self.execute(statement)
  File ".../aiosqlite/core.py", line 223, in execute
    cursor = await self._execute(self._conn.execute, sql, parameters)
sqlite3.OperationalError: database is locked
```

Startup log shortly before the failure:
```txt
Waiting for integrations to complete setup:
{('zha', '01K99WZPV04Y4WJVKYQC26RT2D'): ..., ('homeassistant_sky_connect', '01K80RMKX8QZRN2NQWR44QR51Q'): ...}
```

## Additional information
- ZBT-1 firmware: SL-OPENTHREAD/2.7.2.0 (owner: otbr), ZBT-2 firmware: EZSP 7.5.1.0.
- Possibly related: zigpy 2.4.0 introduced batching of DB writes (PR #1835,
  `database_commit_interval`, default 30 s). Its description notes that a
  second process writing to `zigbee.db` while zigpy is running may now get
  `database is locked`, because transactions can stay open for up to 30 s.
  This install runs zigpy 2.4.1, so it includes that change. I have not
  verified that it is the cause.
- Expected: a hardware entry whose device is not ZHA's radio and does not use the
  Multiprotocol add-on does not open ZHA's database. Suggested fixes:
  - In `_register_multipan_platform`, call `async_using_multipan` first and only
    call `async_get_channel` if it is true.
  - Or, in `multi_pan_addon_using_device`, check the add-on state before
    creating the manager.
  - Independently, ZHA's setup could raise `ConfigEntryNotReady` on a locked DB so
    that HA retries instead of leaving the entry in `setup_error`.
- Workaround: reload the ZHA config entry.
