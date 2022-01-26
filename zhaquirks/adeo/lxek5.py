"""Device handler for ADEO LXEK-5 (HR-C99C-Z-C045) Remote."""
from zigpy.profiles import zha
from zigpy.quirks import CustomDevice
from zigpy.zcl import foundation
from zigpy.zcl.clusters.general import (
    Basic,
    Groups,
    Identify,
    LevelControl,
    OnOff,
    Ota,
    PowerConfiguration,
)
from zigpy.zcl.clusters.homeautomation import Diagnostic
from zigpy.zcl.clusters.lightlink import LightLink
from zigpy.zcl.clusters.lighting import Color

from zhaquirks import EventableCluster, Bus
from zhaquirks.const import (
    ARGS,
    BUTTON_1,
    BUTTON_2,
    BUTTON_3,
    BUTTON_4,
    CLUSTER_ID,
    COMMAND,
    COMMAND_OFF,
    COMMAND_ON,
    COMMAND_STEP,
    COMMAND_STEP_COLOR_TEMP,
    COMMAND_STEP_HUE,
    COMMAND_STEP_SATURATION,
    DEVICE_TYPE,
    DIM_DOWN,
    DIM_UP,
    ENDPOINTS,
    ENDPOINT_ID,
    INPUT_CLUSTERS,
    MODELS_INFO,
    OUTPUT_CLUSTERS,
    PROFILE_ID,
    SHORT_PRESS,
    TURN_OFF,
    TURN_ON,
    ZHA_SEND_EVENT,
)
import zigpy.types as t
from typing import Any, List, Optional, Union

COLOR_UP = "color_up"
COLOR_DOWN = "color_down"
SATURATION_UP = "saturation_up"
SATURATION_DOWN = "saturation_down"
HUE_LEFT = "hue_left"
HUE_RIGHT = "hue_right"

MANUFACTURER_SPECIFIC_CLUSTER_ID_PRESET = 0xFE00  # decimal = 65024


class AdeoPresetCluster(EventableCluster):
    """Custom cluster for preset buttons 1-4"""

    cluster_id = MANUFACTURER_SPECIFIC_CLUSTER_ID_PRESET
    name = "AdeoPresetCluster"
    ep_attribute = "adeo_preset_cluster"
    manufacturer_client_commands = {0x000: ("preset", (t.uint8_t, t.uint8_t), False)}

    def handle_cluster_request(
        self,
        hdr: foundation.ZCLHeader,
        args: List[Any],
        *,
        dst_addressing: Optional[
            Union[t.Addressing.Group, t.Addressing.IEEE, t.Addressing.NWK]
        ] = None,
    ):
        """Send cluster client requests as events."""
        if (
            self.manufacturer_client_commands is not None
            and self.manufacturer_client_commands.get(hdr.command_id) is not None
        ):
            self.listener_event(
                ZHA_SEND_EVENT,
                self.manufacturer_client_commands.get(hdr.command_id)[0],
                args,
            )
            self.debug(
                "AdeoPresetCluster : fire event {action=%s, args=%s}",
                self.manufacturer_client_commands.get(hdr.command_id)[0],
                str(args),
            )
        else:
            self.debug("AdeoPresetCluster : NO event fired")
            super().handle_cluster_request(hdr, args, dst_addressing=dst_addressing)


class AdeoLxek5(CustomDevice):
    """Custom device representing ADEO LXEK-5 Remote."""

    signature = {
        #  <SimpleDescriptor endpoint=1 profile=260 device_type=2048
        #  device_version=1
        #  input_clusters=[0, 1, 3, 2821, 4096, 64769]
        #  output_clusters=[3, 4, 6, 8, 25, 768, 4096]>
        MODELS_INFO: [("ADEO", "LXEK-5")],
        ENDPOINTS: {
            1: {
                PROFILE_ID: zha.PROFILE_ID,  # 260
                DEVICE_TYPE: zha.DeviceType.COLOR_CONTROLLER,  # 2048
                INPUT_CLUSTERS: [
                    Basic.cluster_id,  # 0
                    PowerConfiguration.cluster_id,  # 1
                    Identify.cluster_id,  # 3
                    Diagnostic.cluster_id,  # 2821
                    LightLink.cluster_id,  # 4096
                    0xFD01,  # 64769
                ],
                OUTPUT_CLUSTERS: [
                    Identify.cluster_id,  # 3
                    Groups.cluster_id,  # 4
                    OnOff.cluster_id,  # 6
                    LevelControl.cluster_id,  # 8
                    Ota.cluster_id,  # 25
                    Color.cluster_id,  # 768
                    LightLink.cluster_id,  # 4096
                ],
            }
        },
    }

    replacement = {
        ENDPOINTS: {
            1: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: zha.DeviceType.COLOR_CONTROLLER,
                INPUT_CLUSTERS: [
                    Basic.cluster_id,  # 0
                    PowerConfiguration.cluster_id,  # 1
                    Identify.cluster_id,  # 3
                    Diagnostic.cluster_id,  # 2821
                    LightLink.cluster_id,  # 4096
                    0xFD01,  # 64769
                ],
                OUTPUT_CLUSTERS: [
                    Identify.cluster_id,  # 3
                    Groups.cluster_id,  # 4
                    OnOff.cluster_id,  # 6
                    LevelControl.cluster_id,  # 8
                    Ota.cluster_id,  # 25
                    Color.cluster_id,  # 768
                    LightLink.cluster_id,  # 4096
                    AdeoPresetCluster,  # 65024
                ],
            }
        },
    }

    device_automation_triggers = {
        (SHORT_PRESS, TURN_ON): {
            COMMAND: COMMAND_ON,
            CLUSTER_ID: 6,  # OnOff.cluster_id
            ENDPOINT_ID: 1,
            ARGS: [],
        },
        (SHORT_PRESS, TURN_OFF): {
            COMMAND: COMMAND_OFF,
            CLUSTER_ID: 6,  # OnOff.cluster_id
            ENDPOINT_ID: 1,
            ARGS: [],
        },
        (SHORT_PRESS, DIM_UP): {
            COMMAND: COMMAND_STEP,
            CLUSTER_ID: 8,  # LevelControl.cluster_id
            ENDPOINT_ID: 1,
            ARGS: [0, 26, 5],
        },
        (SHORT_PRESS, DIM_DOWN): {
            COMMAND: COMMAND_STEP,
            CLUSTER_ID: 8,  # LevelControl.cluster_id
            ENDPOINT_ID: 1,
            ARGS: [1, 26, 5],
        },
        (SHORT_PRESS, COLOR_UP): {
            COMMAND: COMMAND_STEP_COLOR_TEMP,
            CLUSTER_ID: 768,  # Color.cluster_id
            ENDPOINT_ID: 1,
            ARGS: [3, 22, 5, 153, 370],
        },
        (SHORT_PRESS, COLOR_DOWN): {
            COMMAND: COMMAND_STEP_COLOR_TEMP,
            CLUSTER_ID: 768,  # Color.cluster_id
            ENDPOINT_ID: 1,
            ARGS: [1, 22, 5, 153, 370],
        },
        (SHORT_PRESS, SATURATION_UP): {
            COMMAND: COMMAND_STEP_SATURATION,
            CLUSTER_ID: 768,  # Color.cluster_id
            ENDPOINT_ID: 1,
            ARGS: [1, 26, 5],
        },
        (SHORT_PRESS, SATURATION_DOWN): {
            COMMAND: COMMAND_STEP_SATURATION,
            CLUSTER_ID: 768,  # Color.cluster_id
            ENDPOINT_ID: 1,
            ARGS: [3, 26, 5],
        },
        (SHORT_PRESS, HUE_LEFT): {
            COMMAND: COMMAND_STEP_HUE,
            CLUSTER_ID: 768,  # Color.cluster_id
            ENDPOINT_ID: 1,
            ARGS: [3, 22, 5],
        },
        (SHORT_PRESS, HUE_RIGHT): {
            COMMAND: COMMAND_STEP_HUE,
            CLUSTER_ID: 768,  # Color.cluster_id
            ENDPOINT_ID: 1,
            ARGS: [1, 22, 5],
        },
        (SHORT_PRESS, BUTTON_1): {
            COMMAND: "preset",
            CLUSTER_ID: 65024,  # AdeoPresetCluster.cluster_id
            ENDPOINT_ID: 1,
            ARGS: [10, 1],
        },
        (SHORT_PRESS, BUTTON_2): {
            COMMAND: "preset",
            CLUSTER_ID: 65024,  # AdeoPresetCluster.cluster_id
            ENDPOINT_ID: 1,
            ARGS: [11, 1],
        },
        (SHORT_PRESS, BUTTON_3): {
            COMMAND: "preset",
            CLUSTER_ID: 65024,  # AdeoPresetCluster.cluster_id
            ENDPOINT_ID: 1,
            ARGS: [12, 1],
        },
        (SHORT_PRESS, BUTTON_4): {
            COMMAND: "preset",
            CLUSTER_ID: 65024,  # AdeoPresetCluster.cluster_id
            ENDPOINT_ID: 1,
            ARGS: [13, 1],
        },
    }
