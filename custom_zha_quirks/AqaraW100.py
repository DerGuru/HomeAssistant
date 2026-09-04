"""Standalone ZHA quirk for the Aqara Climate Sensor W100.

Model: lumi.sensor_ht.agl001

Provides:
- Temperature
- Relative humidity
- Battery percentage from Aqara heartbeat tag 102
- Single, double, hold and release events for all three buttons
"""

from zigpy.zcl import foundation

from zhaquirks.builder import QuirkBuilder
from zhaquirks.const import (
    COMMAND,
    DOUBLE_PRESS,
    LONG_PRESS,
    LONG_RELEASE,
    SHORT_PRESS,
)
from zhaquirks.xiaomi import (
    AQARA,
    BATTERY_PERCENTAGE_REMAINING_ATTRIBUTE,
    RelativeHumidityCluster,
    TemperatureMeasurementCluster,
    XiaomiAqaraE1Cluster,
    XiaomiPowerConfiguration,
)
from zhaquirks.xiaomi.aqara.opple_remote import (
    COMMAND_1_DOUBLE,
    COMMAND_1_HOLD,
    COMMAND_1_RELEASE,
    COMMAND_1_SINGLE,
    COMMAND_2_DOUBLE,
    COMMAND_2_HOLD,
    COMMAND_2_RELEASE,
    COMMAND_2_SINGLE,
    COMMAND_3_DOUBLE,
    COMMAND_3_HOLD,
    COMMAND_3_RELEASE,
    COMMAND_3_SINGLE,
    MultistateInputCluster,
)


PLUS_BUTTON = "plus"
CENTER_BUTTON = "center"
MINUS_BUTTON = "minus"


class W100PowerConfiguration(XiaomiPowerConfiguration):
    """Ignore the W100's incorrect standard Zigbee battery reports.

    The standard battery_percentage_remaining attribute reports zero.
    The actual battery value arrives in the Aqara 0xFCC0 heartbeat.
    """

    def handle_cluster_general_request(
        self,
        hdr,
        args,
        *,
        dst_addressing=None,
    ):
        """Drop attribute reports; pass other commands through."""

        if hdr.command_id == foundation.GeneralCommand.Report_Attributes:
            return

        super().handle_cluster_general_request(
            hdr,
            args,
            dst_addressing=dst_addressing,
        )


class W100AqaraE1Cluster(XiaomiAqaraE1Cluster):
    """Parse the W100-specific battery percentage heartbeat field."""

    def _parse_aqara_attributes(self, value):
        """Map heartbeat tag 102 to battery percentage."""

        attributes = super()._parse_aqara_attributes(value)

        # Before the upstream parser change, unknown Aqara heartbeat fields
        # are returned under keys such as "0xff01-102".
        raw_battery_key = "0xff01-102"

        if raw_battery_key in attributes:
            attributes[BATTERY_PERCENTAGE_REMAINING_ATTRIBUTE] = (
                attributes.pop(raw_battery_key)
            )

        return attributes


(
    QuirkBuilder(AQARA, "lumi.sensor_ht.agl001")
    .friendly_name(
        manufacturer="Aqara",
        model="Climate Sensor W100",
    )

    # Standard sensor clusters
    .replaces(TemperatureMeasurementCluster)
    .replaces(RelativeHumidityCluster)

    # Battery handling
    .replaces(W100PowerConfiguration)
    .replaces(W100AqaraE1Cluster)

    # Buttons on endpoints 1, 2 and 3
    .replaces(MultistateInputCluster)
    .replaces(MultistateInputCluster, endpoint_id=2)
    .replaces(MultistateInputCluster, endpoint_id=3)

    # Home Assistant device triggers
    .device_automation_triggers(
        {
            # Plus button
            (SHORT_PRESS, PLUS_BUTTON): {
                COMMAND: COMMAND_1_SINGLE,
            },
            (DOUBLE_PRESS, PLUS_BUTTON): {
                COMMAND: COMMAND_1_DOUBLE,
            },
            (LONG_PRESS, PLUS_BUTTON): {
                COMMAND: COMMAND_1_HOLD,
            },
            (LONG_RELEASE, PLUS_BUTTON): {
                COMMAND: COMMAND_1_RELEASE,
            },

            # Center button
            (SHORT_PRESS, CENTER_BUTTON): {
                COMMAND: COMMAND_2_SINGLE,
            },
            (DOUBLE_PRESS, CENTER_BUTTON): {
                COMMAND: COMMAND_2_DOUBLE,
            },
            (LONG_PRESS, CENTER_BUTTON): {
                COMMAND: COMMAND_2_HOLD,
            },
            (LONG_RELEASE, CENTER_BUTTON): {
                COMMAND: COMMAND_2_RELEASE,
            },

            # Minus button
            (SHORT_PRESS, MINUS_BUTTON): {
                COMMAND: COMMAND_3_SINGLE,
            },
            (DOUBLE_PRESS, MINUS_BUTTON): {
                COMMAND: COMMAND_3_DOUBLE,
            },
            (LONG_PRESS, MINUS_BUTTON): {
                COMMAND: COMMAND_3_HOLD,
            },
            (LONG_RELEASE, MINUS_BUTTON): {
                COMMAND: COMMAND_3_RELEASE,
            },
        }
    )
    .add_to_registry()
)