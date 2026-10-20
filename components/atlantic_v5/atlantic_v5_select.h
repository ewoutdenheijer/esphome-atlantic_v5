// L3 ESPHome glue for selects that write shared runtime state (RelayPolicy),
// unlike the read-only sensor/binary_sensor/text_sensor platforms.
#pragma once

// Included before the USE_SELECT check below: this header is the first thing
// atlantic_v5_select.cpp includes, so nothing has pulled defines.h in yet -
// unlike ESPHome's generated main.cpp, which reaches USE_SELECT already
// defined via its own earlier includes.
#include "esphome/core/defines.h"

#ifdef USE_SELECT

#include "esphome/components/select/select.h"
#include "esphome/core/component.h"
#include "esphome/core/helpers.h"

#include "atlantic_v5.h"

namespace esphome {
namespace atlantic_v5_component {

class AtlanticV5Select : public Component, public select::Select, public Parented<AtlanticV5Component> {
 public:
  void setup() override;

 protected:
  void control(size_t index) override;
};

class AtlanticV5CompressorSelect : public Component, public select::Select, public Parented<AtlanticV5Component> {
 public:
  void setup() override;

 protected:
  void control(size_t index) override;
};

class AtlanticV5HeatingElementSelect : public Component, public select::Select, public Parented<AtlanticV5Component> {
 public:
  void setup() override;

 protected:
  void control(size_t index) override;
};

}  // namespace atlantic_v5_component
}  // namespace esphome

#endif  // USE_SELECT
