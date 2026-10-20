import esphome.codegen as cg
from esphome import final_validate
from esphome.components import select
import esphome.config_validation as cv

from . import CONF_ATLANTIC_V5_ID, CONF_MODE, MODE_MITM, AtlanticV5Component, atlantic_v5_ns

DEPENDENCIES = ["atlantic_v5"]
CODEOWNERS = ["@jsimonetti"]

# Controllable entities (ADR 0001) write into the hub's RelayPolicy, so they
# get dedicated classes instead of the read-only platforms' generic table.
AtlanticV5Select = atlantic_v5_ns.class_("AtlanticV5Select", select.Select, cg.Component)
AtlanticV5CompressorSelect = atlantic_v5_ns.class_(
    "AtlanticV5CompressorSelect", select.Select, cg.Component
)

CONF_CONTROL_MODE = "control_mode"
CONF_COMPRESSOR_MODE = "compressor_mode"

# The control surface's modes (docs/protocol.md), in ControlMode enum order
# (types.h): the option's index is the wire value the rewrite hook applies, so
# no string lookup is needed on the hot control path.
OPTION_PASSTHROUGH = "passthrough"
OPTION_NORMAL = "normal"
OPTION_EAGER = "eager"
OPTION_OFF = "off"
OPTION_BOOST = "boost"
OPTIONS = [OPTION_PASSTHROUGH, OPTION_NORMAL, OPTION_EAGER, OPTION_OFF, OPTION_BOOST]
COMPRESSOR_OPTIONS = ["auto", "off", "on"]

CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(CONF_ATLANTIC_V5_ID): cv.use_id(AtlanticV5Component),
        cv.Optional(CONF_CONTROL_MODE): select.select_schema(AtlanticV5Select),
        cv.Optional(CONF_COMPRESSOR_MODE): select.select_schema(AtlanticV5CompressorSelect),
    }
)


def _final_validate(config):
    configured = [key for key in (CONF_CONTROL_MODE, CONF_COMPRESSOR_MODE) if key in config]
    if not configured:
        return
    fconf = final_validate.full_config.get()
    hub_path = fconf.get_path_for_id(config[CONF_ATLANTIC_V5_ID])[:-1]
    hub_conf = fconf.get_config_for_path(hub_path)
    if hub_conf[CONF_MODE] != MODE_MITM:
        if CONF_CONTROL_MODE in configured:
            raise cv.Invalid(
                "control_mode requires atlantic_v5 mode: mitm (rewriting frames only works in MITM mode)",
                path=[CONF_CONTROL_MODE],
            )
        if CONF_COMPRESSOR_MODE in configured:
            raise cv.Invalid(
                "compressor_mode requires atlantic_v5 mode: mitm (rewriting frames only works in MITM mode)",
                path=[CONF_COMPRESSOR_MODE],
            )


FINAL_VALIDATE_SCHEMA = _final_validate


async def to_code(config):
    hub = await cg.get_variable(config[CONF_ATLANTIC_V5_ID])
    if CONF_CONTROL_MODE in config:
        conf = config[CONF_CONTROL_MODE]
        var = await select.new_select(conf, options=OPTIONS)
        await cg.register_component(var, conf)
        cg.add(var.set_parent(hub))

    if CONF_COMPRESSOR_MODE in config:
        conf = config[CONF_COMPRESSOR_MODE]
        var = await select.new_select(conf, options=COMPRESSOR_OPTIONS)
        await cg.register_component(var, conf)
        cg.add(var.set_parent(hub))
