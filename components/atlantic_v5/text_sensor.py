import esphome.codegen as cg
from esphome.components import text_sensor
import esphome.config_validation as cv
from esphome.const import ENTITY_CATEGORY_DIAGNOSTIC

from . import CONF_ATLANTIC_V5_ID, AtlanticV5Component, EntityKind

DEPENDENCIES = ["atlantic_v5"]
CODEOWNERS = ["@jsimonetti"]

# key (message catalogue's Entity name, docs/protocol.md) -> EntityId enum member
# name in catalog.h.
TEXT_SENSORS = {
    "controller_firmware_version": "ENT_CONTROLLER_FIRMWARE_VERSION",
    "appliance_serial": "ENT_APPLIANCE_SERIAL",
    "product_code": "ENT_PRODUCT_CODE",
    "power_board_version": "ENT_POWER_BOARD_VERSION",
    "controller_model": "ENT_CONTROLLER_MODEL",
    "hmi_firmware_version": "ENT_HMI_FIRMWARE_VERSION",
    "hmi_model": "ENT_HMI_MODEL",
    "frame_0164006401": "ENT_FRAME_0164006401",
    "frame_0164006501": "ENT_FRAME_0164006501",
    "frame_0164006601": "ENT_FRAME_0164006601",
    "frame_0164006701": "ENT_FRAME_0164006701",
    "frame_0164006e01": "ENT_FRAME_0164006E01",
    "frame_016414b701": "ENT_FRAME_016414B701",
    "frame_0164158301": "ENT_FRAME_0164158301",
    "frame_0164feb006": "ENT_FRAME_0164FEB006",
    "frame_0164feba03": "ENT_FRAME_0164FEBA03",
    "frame_0164febd03": "ENT_FRAME_0164FEBD03",
    "frame_0164fec003": "ENT_FRAME_0164FEC003",
    "frame_0164fec303": "ENT_FRAME_0164FEC303",
    "frame_0164fec603": "ENT_FRAME_0164FEC603",
    "frame_0164fec903": "ENT_FRAME_0164FEC903",
    "frame_0164fee203": "ENT_FRAME_0164FEE203",
    "frame_0164fee503": "ENT_FRAME_0164FEE503",
    "frame_0164fee803": "ENT_FRAME_0164FEE803",
    "frame_0164feeb03": "ENT_FRAME_0164FEEB03",
    "frame_0164feee03": "ENT_FRAME_0164FEEE03",
    "frame_0164fef103": "ENT_FRAME_0164FEF103",
    "frame_0164ff1403": "ENT_FRAME_0164FF1403",
    "frame_0165000301": "ENT_FRAME_0165000301",
    "frame_0165000a01": "ENT_FRAME_0165000A01",
    "frame_0165fef701": "ENT_FRAME_0165FEF701",
    "frame_0164007001": "ENT_FRAME_0164007001",
    "frame_0164007101": "ENT_FRAME_0164007101",
    "frame_0164007501": "ENT_FRAME_0164007501",
    "frame_01640165fe": "ENT_FRAME_01640165FE",
    "frame_0164152a01": "ENT_FRAME_0164152A01",
    "frame_016421b601": "ENT_FRAME_016421B601",
    "frame_016443130d": "ENT_FRAME_016443130D",
    "frame_0164fded01": "ENT_FRAME_0164FDED01",
    "frame_0164fdee01": "ENT_FRAME_0164FDEE01",
    "frame_0164fdfa01": "ENT_FRAME_0164FDFA01",
    "frame_0164fdfd01": "ENT_FRAME_0164FDFD01",
    "frame_0164fe0001": "ENT_FRAME_0164FE0001",
    "frame_0164fed801": "ENT_FRAME_0164FED801",
    "frame_0164ffdc01": "ENT_FRAME_0164FFDC01",
    "frame_0165152301": "ENT_FRAME_0165152301",
    "frame_016516b301": "ENT_FRAME_016516B301",
    "frame_0165fdf802": "ENT_FRAME_0165FDF802",
    "frame_0165fdfb02": "ENT_FRAME_0165FDFB02",
    "frame_0165fdfe02": "ENT_FRAME_0165FDFE02",
    "frame_0165fef901": "ENT_FRAME_0165FEF901",
    "frame_0165fefb01": "ENT_FRAME_0165FEFB01",
    "frame_0165fefd01": "ENT_FRAME_0165FEFD01",
    "frame_0165feff01": "ENT_FRAME_0165FEFF01",
    "frame_0165ff0101": "ENT_FRAME_0165FF0101",
    "frame_0165ff0301": "ENT_FRAME_0165FF0301",
    "unknown_frame": "ENT_UNKNOWN_FRAME",
}

CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(CONF_ATLANTIC_V5_ID): cv.use_id(AtlanticV5Component),
        **{
            cv.Optional(key): text_sensor.text_sensor_schema(entity_category=ENTITY_CATEGORY_DIAGNOSTIC)
            for key in TEXT_SENSORS
        },
    }
)


async def to_code(config):
    hub = await cg.get_variable(config[CONF_ATLANTIC_V5_ID])
    for key, ent_id in TEXT_SENSORS.items():
        if key not in config:
            continue
        sens = await text_sensor.new_text_sensor(config[key])
        # See sensor.py's comment: leading `::` disambiguates the L1/L2 core's
        # global `atlantic_v5` namespace from this file's `esphome::atlantic_v5`.
        cg.add(hub.set_entity(cg.RawExpression(f"::atlantic_v5::{ent_id}"), sens, EntityKind.TEXT_SENSOR))
