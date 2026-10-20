#include "catalog.h"

namespace atlantic_v5 {

namespace {
constexpr const char *NAMES[ENT_COUNT] = {
    "controller_firmware_version",
    "appliance_serial",
    "product_code",
    "power_board_version",
    "controller_model",
    "setpoint_min",
    "setpoint_max",
    "water_temperature",
    "compressor_outlet_temperature",
    "air_inlet_temperature",
    "evaporator_1_temperature",
    "evaporator_2_temperature",
    "evaporator_3_temperature",
    "water_temperature_min",
    "water_temperature_max",
    "compressor_outlet_temperature_min",
    "compressor_outlet_temperature_max",
    "air_inlet_temperature_min",
    "air_inlet_temperature_max",
    "evaporator_1_temperature_min",
    "evaporator_1_temperature_max",
    "evaporator_2_temperature_min",
    "evaporator_2_temperature_max",
    "evaporator_3_temperature_min",
    "evaporator_3_temperature_max",
    "cycle_1_active",
    "cycle_1_count",
    "cycle_2_active",
    "cycle_2_count",
    "cycle_3_active",
    "cycle_3_count",
    "cycle_4_active",
    "cycle_4_count",
    "cycle_5_active",
    "cycle_5_count",
    "cycle_6_active",
    "cycle_6_count",
    "input_i2",
    "input_i1",
    "heating_active",
    "hmi_firmware_version",
    "hmi_model",
    "heating_element_active",
    "valid_frames",
    "crc_errors",
    "dropped_bytes",
    "valid_frames_hmi",
    "crc_errors_hmi",
    "dropped_bytes_hmi",
    "valid_frames_main",
    "crc_errors_main",
    "dropped_bytes_main",
    "unknown_frames",
    "frames_relayed",
    "rewrites_applied",
    "queue_overflows",
    "relay_latency_max_us",
    "relay_latency_avg_us",
    "task_stack_free",
    "connected",
    "frame_0164006401",
    "frame_0164006501",
    "frame_0164006601",
    "frame_0164006701",
    "frame_0164006e01",
    "frame_016414b701",
    "frame_0164158301",
    "frame_0164feb006",
    "frame_0164feba03",
    "frame_0164febd03",
    "frame_0164fec003",
    "frame_0164fec303",
    "frame_0164fec603",
    "frame_0164fec903",
    "frame_0164fee203",
    "frame_0164fee503",
    "frame_0164fee803",
    "frame_0164feeb03",
    "frame_0164feee03",
    "frame_0164fef103",
    "frame_0164ff1403",
    "frame_0165000301",
    "frame_0165000a01",
    "frame_0165fef701",
    "frame_0164007001",
    "frame_0164007101",
    "frame_0164007501",
    "frame_01640165fe",
    "frame_0164152a01",
    "frame_016421b601",
    "frame_016443130d",
    "frame_0164fded01",
    "frame_0164fdee01",
    "frame_0164fdfa01",
    "frame_0164fdfd01",
    "frame_0164fe0001",
    "frame_0164fed801",
    "frame_0164ffdc01",
    "frame_0165152301",
    "frame_016516b301",
    "frame_0165fdf802",
    "frame_0165fdfb02",
    "frame_0165fdfe02",
    "frame_0165fef901",
    "frame_0165fefb01",
    "frame_0165fefd01",
    "frame_0165feff01",
    "frame_0165ff0101",
    "frame_0165ff0301",
    "unknown_frame",
};
}  // namespace

const char *entity_name(EntityId id) {
  return id < ENT_COUNT ? NAMES[id] : "unknown";
}

size_t init_cadence_index(uint16_t id) {
  for (size_t i = 0; i < INIT_CADENCE_COUNT; i++)
    if (INIT_CADENCE[i] == id)
      return i;
  return INIT_CADENCE_COUNT;
}

namespace {
bool contains(const uint64_t *keys, size_t n, uint64_t key) {
  size_t lo = 0, hi = n;
  while (lo < hi) {
    size_t mid = lo + (hi - lo) / 2;
    if (keys[mid] == key)
      return true;
    if (keys[mid] < key)
      lo = mid + 1;
    else
      hi = mid;
  }
  return false;
}
}  // namespace

HeaderClass classify_header(uint64_t key) {
  if (contains(header::MAPPED, header::MAPPED_COUNT, key))
    return HeaderClass::MAPPED;
  if (contains(header::UNMAPPED, header::UNMAPPED_COUNT, key))
    return HeaderClass::UNMAPPED;
  return HeaderClass::UNKNOWN;
}

bool is_unmapped_header(uint64_t key) {
  return classify_header(key) == HeaderClass::UNMAPPED;
}

EntityId frame_entity_id(uint64_t key) {
  for (size_t i = 0; i < header::MAPPED_COUNT; i++)
    if (header::MAPPED[i] == key)
      return static_cast<EntityId>(ENT_FRAME_MAPPED_FIRST + i);
  for (size_t i = 0; i < header::UNMAPPED_COUNT; i++)
    if (header::UNMAPPED[i] == key)
      return static_cast<EntityId>(ENT_FRAME_UNMAPPED_FIRST + i);
  return ENT_UNKNOWN_FRAME;
}

}  // namespace atlantic_v5
