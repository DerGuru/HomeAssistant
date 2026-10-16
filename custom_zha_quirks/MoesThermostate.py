"""
ZHA Quirks for Moes (B/Z)HT-002-GA-WH-MS Smart Thermostat.

Fingerprint: modelID 'TS0601', manufacturerName '_TZE204_xalsoe3m'
"""

from zigpy.zcl.clusters.hvac import Thermostat

from zhaquirks.tuya.builder import TuyaQuirkBuilder
from zhaquirks.tuya.mcu import TuyaAttributesCluster

import zigpy.types as t


def _tuya_bool(v) -> bool:
    """Robust bool conversion for Tuya payloads (bool, Bool.true/false, ints, etc.)."""
    try:
        return bool(int(v))
    except Exception:
        return bool(v)


class PresetMode(t.enum8):
    """Operating mode (DP 2); Auto follows the device's internal schedule."""

    Auto = 0x00
    Manual = 0x01


class SensorMode(t.enum8):
    """Sensor used for regulation (DP 32)."""

    Internal = 0x00
    External = 0x01
    Both = 0x02


class MoesThermostatCluster(Thermostat, TuyaAttributesCluster):
    """Like TuyaThermostatV2, but keeps min/max_heat_setpoint_limit so HA follows DP 18/34."""

    _CONSTANT_ATTRIBUTES = {
        # frame for the device-adjustable limits (DP 18: 0–20 °C, DP 34: 20–50 °C)
        Thermostat.AttributeDefs.abs_min_heat_setpoint_limit.id: 0,
        Thermostat.AttributeDefs.abs_max_heat_setpoint_limit.id: 5000,
        Thermostat.AttributeDefs.ctrl_sequence_of_oper.id: Thermostat.ControlSequenceOfOperation.Heating_Only,
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for attr in (
            Thermostat.AttributeDefs.setpoint_change_source,
            Thermostat.AttributeDefs.setpoint_change_source_timestamp,
            Thermostat.AttributeDefs.pi_heating_demand,
            # calibration is exposed via DP 19; hides ZHA's generic ±2.5 °C entity
            Thermostat.AttributeDefs.local_temperature_calibration,
        ):
            self.add_unsupported_attribute(attr.id)


(
    TuyaQuirkBuilder("_TZE204_xalsoe3m", "TS0601")
    .adds(MoesThermostatCluster)

    # DP 1 — ON/OFF (WRITEABLE) -> system_mode
    # IMPORTANT: dp_converter returns True/False so Tuya encodes BOOL, not VALUE(4 bytes)
    .tuya_dp(
        dp_id=1,
        ep_attribute=MoesThermostatCluster.ep_attribute,
        attribute_name=MoesThermostatCluster.AttributeDefs.system_mode.name,
        converter=lambda v: Thermostat.SystemMode.Heat if _tuya_bool(v) else Thermostat.SystemMode.Off,
        dp_converter=lambda m: (m != Thermostat.SystemMode.Off),
    )

    # DP 16 — local_temperature (0.1°C) -> ZCL (0.01°C)
    .tuya_dp(
        dp_id=16,
        ep_attribute=MoesThermostatCluster.ep_attribute,
        attribute_name=MoesThermostatCluster.AttributeDefs.local_temperature.name,
        converter=lambda v: int(v) * 10,
    )
    
    
    # DP 47 — valve_state: true=heating, false=idle (not inverted, verified live)
    .tuya_dp(
        dp_id=47,
        ep_attribute=MoesThermostatCluster.ep_attribute,
        attribute_name=MoesThermostatCluster.AttributeDefs.running_state.name,
        converter=lambda v: _tuya_bool(v)
    )

    # DP 50 — current_heating_setpoint (1°C) -> ZCL (0.01°C)
    .tuya_dp(
        dp_id=50,
        ep_attribute=MoesThermostatCluster.ep_attribute,
        attribute_name=MoesThermostatCluster.AttributeDefs.occupied_heating_setpoint.name,
        converter=lambda v: (int(t.int16s(v)) * 100),
        dp_converter=lambda sp: (t.int16s(int(sp) // 100)),
    )

    # DP 18/34 — device min/max setpoint (1°C) -> ZCL (0.01°C); HA's climate range follows these
    .tuya_dp(
        dp_id=18,
        ep_attribute=MoesThermostatCluster.ep_attribute,
        attribute_name=MoesThermostatCluster.AttributeDefs.min_heat_setpoint_limit.name,
        converter=lambda v: int(v) * 100,
        dp_converter=lambda sp: int(sp) // 100,
    )
    .tuya_dp(
        dp_id=34,
        ep_attribute=MoesThermostatCluster.ep_attribute,
        attribute_name=MoesThermostatCluster.AttributeDefs.max_heat_setpoint_limit.name,
        converter=lambda v: int(v) * 100,
        dp_converter=lambda sp: int(sp) // 100,
    )

    .tuya_enum(
        dp_id=2,
        attribute_name="preset_mode",
        enum_class=PresetMode,
        translation_key="preset_mode",
        fallback_name="Preset mode",
    )
    .tuya_switch(
        dp_id=39,
        attribute_name="child_lock",
        translation_key="child_lock",
        fallback_name="Child lock",
    )
    .tuya_enum(
        dp_id=32,
        attribute_name="temperature_sensor_select",
        enum_class=SensorMode,
        translation_key="sensor_mode",
        fallback_name="Sensor mode",
    )
    .tuya_number(
        dp_id=102,
        attribute_name="deadzone_temperature",
        type=t.uint16_t,
        unit="°C",
        min_value=1,
        max_value=5,
        step=1,
        translation_key="deadzone_temperature",
        fallback_name="Deadzone temperature",
    )
    .tuya_number(
        dp_id=19,
        attribute_name="local_temperature_calibration",
        type=t.int32s,
        unit="°C",
        min_value=-9,
        max_value=9,
        step=1,
        translation_key="local_temperature_calibration",
        fallback_name="Local temperature calibration",
    )

    .tuya_enchantment(data_query_spell=True)
    .skip_configuration()
    .add_to_registry()
)
