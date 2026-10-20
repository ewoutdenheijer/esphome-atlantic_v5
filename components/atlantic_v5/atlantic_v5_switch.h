// L3 ESPHome glue for controllable switches (ADR 0001). Each feature is
// compile-time opt-in through switch.py, so unconfigured controls are absent.
#pragma once

// Included before the USE_SWITCH check below for the same reason as in
// atlantic_v5_select.h: this header is the first thing atlantic_v5_switch.cpp
// includes, so nothing has pulled defines.h in yet.
#include "esphome/core/defines.h"

#if defined(USE_SWITCH) && \
    (defined(ATLANTIC_V5_LINK_BLACKOUT) || defined(ATLANTIC_V5_HEATING_ELEMENT_OVERRIDE))

#include "esphome/components/switch/switch.h"
#include "esphome/core/component.h"
#include "esphome/core/helpers.h"

#include "atlantic_v5.h"

namespace esphome {
namespace atlantic_v5_component {

#ifdef ATLANTIC_V5_LINK_BLACKOUT
class AtlanticV5LinkBlackoutSwitch : public Component, public switch_::Switch, public Parented<AtlanticV5Component> {
 public:
  void setup() override;
  void loop() override;

 protected:
  void write_state(bool state) override;
};
#endif

#ifdef ATLANTIC_V5_HEATING_ELEMENT_OVERRIDE
class AtlanticV5HeatingElementSwitch : public Component, public switch_::Switch,
                                       public Parented<AtlanticV5Component> {
 public:
  void setup() override;

 protected:
  void write_state(bool state) override;
};
#endif

}  // namespace atlantic_v5_component
}  // namespace esphome

#endif  // USE_SWITCH && (ATLANTIC_V5_LINK_BLACKOUT || ATLANTIC_V5_HEATING_ELEMENT_OVERRIDE)
