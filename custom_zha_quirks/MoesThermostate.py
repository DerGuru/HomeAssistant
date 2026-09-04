"""
ZHA Quirks for Moes BHT-002-GCLZB Smart Thermostat.

Fingerprint: modelID 'TS0601', manufacturerName '_TZE204_xalsoe3m'
"""

from zigpy.zcl.clusters.hvac import Thermostat

from zhaquirks.tuya.builder import TuyaQuirkBuilder
from zhaquirks.tuya.tuya_trv import TuyaThermostatV2

import zigpy.types as t


def _tuya_bool(v) -> bool:
    """Robust bool conversion for Tuya payloads (bool, Bool.true/false, ints, etc.)."""
    try:
        return bool(int(v))
    except Exception:
        return bool(v)


(
    TuyaQuirkBuilder("_TZE204_xalsoe3m", "TS0601")
    .adds(TuyaThermostatV2)

    # DP 1 — ON/OFF (WRITEABLE) -> system_mode
    # IMPORTANT: dp_converter returns True/False so Tuya encodes BOOL, not VALUE(4 bytes)
    .tuya_dp(
        dp_id=1,
        ep_attribute=TuyaThermostatV2.ep_attribute,
        attribute_name=TuyaThermostatV2.AttributeDefs.system_mode.name,
        converter=lambda v: Thermostat.SystemMode.Heat if _tuya_bool(v) else Thermostat.SystemMode.Off,
        dp_converter=lambda m: (m != Thermostat.SystemMode.Off),
    )

    # DP 16 — local_temperature (0.1°C) -> ZCL (0.01°C)
    .tuya_dp(
        dp_id=16,
        ep_attribute=TuyaThermostatV2.ep_attribute,
        attribute_name=TuyaThermostatV2.AttributeDefs.local_temperature.name,
        converter=lambda v: int(v) * 10,
    )
    
    
    # DP 47 — valve_state: heating active (inverted: true=off, false=on)
    .tuya_dp(
        dp_id=47,
        ep_attribute=TuyaThermostatV2.ep_attribute,
        attribute_name=TuyaThermostatV2.AttributeDefs.running_state.name,
        converter=lambda v: _tuya_bool(v)
    )

    # DP 50 — current_heating_setpoint (1°C) -> ZCL (0.01°C)
    .tuya_dp(
        dp_id=50,
        ep_attribute=TuyaThermostatV2.ep_attribute,
        attribute_name=TuyaThermostatV2.AttributeDefs.occupied_heating_setpoint.name,
        converter=lambda v: (int(t.int16s(v)) * 100),
        dp_converter=lambda sp: (t.int16s(int(sp) // 100)),
    )

    .tuya_enchantment(data_query_spell=True)
    .skip_configuration()
    .add_to_registry()
)
