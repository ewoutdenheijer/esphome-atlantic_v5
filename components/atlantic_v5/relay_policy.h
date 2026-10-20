// L1 core. Host-compilable: no esp-idf, no ESPHome, no Arduino, no exceptions, no heap.
#pragma once

#include <atomic>

#include "frame.h"
#include "types.h"

namespace atlantic_v5 {

// The bus rewrites supported by this component (docs/protocol.md "Control
// surface"). Runtime controls are written from the main loop and read by the
// relay task/thread, hence atomics rather than a lock.
class RelayPolicy {
 public:
  static constexpr uint64_t INPUT_STATUS_HEADER_KEY = 0x0164FF1403ULL;
  static constexpr uint8_t INPUT_STATUS_PAYLOAD_LEN = REWRITE_PAYLOAD_LEN;
  static constexpr uint64_t HEATING_ELEMENT_HEADER_KEY = 0x0165FEF701ULL;
  static constexpr uint8_t HEATING_ELEMENT_PAYLOAD_LEN = 1;
  static constexpr uint64_t COMPRESSOR_COMMAND_HEADER_KEY = 0x0165FEF901ULL;
  static constexpr uint8_t COMPRESSOR_COMMAND_PAYLOAD_LEN = 1;

  void set_control_mode(ControlMode m) { mode_.store(static_cast<uint8_t>(m), std::memory_order_relaxed); }
  ControlMode control_mode() const {
    return static_cast<ControlMode>(mode_.load(std::memory_order_relaxed));
  }
  void set_compressor_mode(CompressorMode m) {
    compressor_mode_.store(static_cast<uint8_t>(m), std::memory_order_relaxed);
  }
  void set_heating_element_active(bool active) {
    heating_element_value_.store(active ? 0x64 : 0x00, std::memory_order_relaxed);
  }

  // Rewrites a supported command payload in place and returns true if it did
  // so. A no-op (returns false, f untouched) unless the header, payload length
  // and CRC all match exactly. The heating-element command is untouched until
  // a command-specific override is enabled.
  bool apply(Frame &f) const;

 private:
  std::atomic<uint8_t> mode_{static_cast<uint8_t>(ControlMode::PASSTHROUGH)};
  std::atomic<uint8_t> compressor_mode_{static_cast<uint8_t>(CompressorMode::AUTO)};
  std::atomic<uint8_t> heating_element_value_{0xFF};
};

}  // namespace atlantic_v5
