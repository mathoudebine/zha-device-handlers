"""Device handler for ADEO LXEK-5 (HR-C99C-Z-C045) Remote."""
from zigpy.profiles import zha
from zigpy.quirks import CustomDevice
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

from zhaquirks.const import (
    ARGS,
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
)

COLOR_UP = "color_up"
COLOR_DOWN = "color_down"
SATURATION_UP = "saturation_up"
SATURATION_DOWN = "saturation_down"
HUE_LEFT = "hue_left"
HUE_RIGHT = "hue_right"

MANUFACTURER_SPECIFIC_CLUSTER_ID_SCENES = 0xFE00  # decimal = 65024


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
                    MANUFACTURER_SPECIFIC_CLUSTER_ID_SCENES,
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
    }
