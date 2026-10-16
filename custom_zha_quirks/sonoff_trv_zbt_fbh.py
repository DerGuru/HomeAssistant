"""SONOFF TRV-ZBT (Gen2): focused ZHA custom quirk for valve control.

Install as /config/custom_zha_quirks/sonoff_trv_zbt_fbh.py and configure:
  zha:
    custom_quirks_path: /config/custom_zha_quirks
Restart Home Assistant. Do not install alongside another TRV-ZBT custom quirk.

Protocol reference: zigpy/zha-device-handlers PR #5234, commit
1de0c2950dccb301ac357a2a90e387625e1790f0 (open at creation, 2026-10-15).
https://github.com/zigpy/zha-device-handlers/pull/5234
https://www.zigbee2mqtt.io/devices/TRV-ZBT.html

Tested locally with zha-quirks 2.3.0 / zigpy 2.3.0; NOT hardware-tested.
Only matches SONOFF / TRV-ZBT, not TRVZB or TRV-ZBM.

Use Manual mode, disable Adaptive mode and Open window detection for external
position experiments. Heating and Idle valve opening both represent OPENING
percentages on Gen2. Setting both to x is an experimental position override,
not a native manual-position mode or a measured physical-position feedback.
Firmware protections/temporary modes may still take precedence. Verify flow.
No automatic writes, calibration, full-stroke cycles or polling on startup.
Calibration is performed only when the user presses the calibration button.
"""

import zigpy.types as t
from zigpy.zcl.clusters.hvac import Thermostat
from zigpy.zcl.foundation import BaseAttributeDefs, ZCLAttributeDef
from zhaquirks.builder import EntityType, QuirkBuilder
from zhaquirks.clusters import CustomCluster


class OperatingMode(t.enum8):
    Off = 0
    Auto = 1
    Manual = 4


class SonoffTRVZBTValveCluster(CustomCluster):
    """Gen2 private attributes; no manufacturer code in the ZCL header."""

    cluster_id = 0xFC11
    ep_attribute = "sonoff_trv_zbt_valve"

    class AttributeDefs(BaseAttributeDefs):
        child_lock = ZCLAttributeDef(
            id=0x0000, type=t.Bool, access="rw", manufacturer_code=None
        )
        open_window = ZCLAttributeDef(
            id=0x6000, type=t.Bool, access="rw", manufacturer_code=None
        )
        heating_valve_position = ZCLAttributeDef(
            id=0x600B, type=t.uint8_t, access="rw", manufacturer_code=None
        )
        idle_valve_position = ZCLAttributeDef(
            id=0x600C, type=t.uint8_t, access="rw", manufacturer_code=None
        )
        temperature_control_mode = ZCLAttributeDef(
            id=0x6013, type=t.enum8, access="rw", manufacturer_code=None
        )
        valve_travel_calibration = ZCLAttributeDef(
            id=0x6036, type=t.Bool, access="w", manufacturer_code=None
        )
        calibration_status = ZCLAttributeDef(
            id=0x6037, type=t.uint8_t, access="rp", manufacturer_code=None
        )

    async def write_attributes(self, attributes, manufacturer=None, **kwargs):
        """Reject invalid valve percentages, including raw cluster writes."""
        for key, value in attributes.items():
            if key in ("heating_valve_position", "idle_valve_position", 0x600B, 0x600C):
                if isinstance(value, bool) or not isinstance(value, int) or not 0 <= value <= 100:
                    raise ValueError("Valve opening must be an integer from 0 to 100")
        return await super().write_attributes(attributes, manufacturer=manufacturer, **kwargs)


def calibration_status(value):
    """Report only values actually received; do not assume startup success."""
    return {0: "Normal", 1: "Failed"}.get(int(value), f"Unknown ({value})")


builder = (
    QuirkBuilder("SONOFF", "TRV-ZBT")
    .replaces(SonoffTRVZBTValveCluster)
    .enum(
        "system_mode", OperatingMode, Thermostat.cluster_id,
        translation_key="trv_zbt_operating_mode", fallback_name="Operating mode",
    )
    .switch(
        "temperature_control_mode", 0xFC11, on_value=2, off_value=1,
        translation_key="trv_zbt_adaptive", fallback_name="Adaptive mode",
    )
    .switch(
        "open_window", 0xFC11,
        translation_key="trv_zbt_open_window", fallback_name="Open window detection",
    )
    .switch(
        "child_lock", 0xFC11,
        translation_key="trv_zbt_child_lock", fallback_name="Child lock",
    )
)
for attribute, label in (
    ("heating_valve_position", "Heating valve opening"),
    ("idle_valve_position", "Idle valve opening"),
):
    builder = builder.number(
        attribute, 0xFC11, min_value=0, max_value=100, step=1, unit="%",
        entity_type=EntityType.STANDARD, initially_disabled=False,
        translation_key=f"trv_zbt_{attribute}", fallback_name=label,
    )

QUIRK = (
    builder.sensor(
        "calibration_status", 0xFC11, attribute_converter=calibration_status,
        entity_type=EntityType.DIAGNOSTIC,
        translation_key="trv_zbt_calibration_status", fallback_name="Calibration status",
    )
    .write_attr_button(
        attribute_name="valve_travel_calibration", cluster_id=0xFC11, attribute_value=1,
        unique_id_suffix="trv_zbt_calibrate_valve",
        translation_key="trv_zbt_calibrate_valve", fallback_name="Calibrate valve",
    )
    .add_to_registry()
)
