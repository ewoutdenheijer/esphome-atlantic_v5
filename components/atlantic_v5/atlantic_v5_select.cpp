#include "atlantic_v5_select.h"

#ifdef USE_SELECT

#include "types.h"

namespace esphome {
namespace atlantic_v5_component {

// Options are declared in select.py in ControlMode enum order (PASSTHROUGH=0
// .. BOOST=4, per docs/protocol.md "Control surface"), so the index IS the
// ControlMode value - no string lookup needed on the control path.
void AtlanticV5Select::setup() { this->publish_state(this->option_at(0)); }

void AtlanticV5Select::control(size_t index) {
  this->publish_state(index);
  this->parent_->set_control_mode(static_cast<::atlantic_v5::ControlMode>(index));
}

void AtlanticV5CompressorSelect::setup() {
  this->parent_->set_compressor_mode(::atlantic_v5::CompressorMode::PASSTHROUGH);
  this->publish_state(this->option_at(0));
}

// Compressor options follow CompressorMode enum order: PASSTHROUGH, OFF, ON.
void AtlanticV5CompressorSelect::control(size_t index) {
  this->publish_state(index);
  this->parent_->set_compressor_mode(static_cast<::atlantic_v5::CompressorMode>(index));
}

void AtlanticV5HeatingElementSelect::setup() {
  this->parent_->set_heating_element_mode(::atlantic_v5::HeatingElementMode::PASSTHROUGH);
  this->publish_state(this->option_at(0));
}

// Heating-element options follow HeatingElementMode enum order.
void AtlanticV5HeatingElementSelect::control(size_t index) {
  this->publish_state(index);
  this->parent_->set_heating_element_mode(static_cast<::atlantic_v5::HeatingElementMode>(index));
}

}  // namespace atlantic_v5_component
}  // namespace esphome

#endif  // USE_SELECT
