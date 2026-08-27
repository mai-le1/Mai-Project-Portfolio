# Autonomous Delivery System — Pico Firmware

MicroPython code for the university autonomous delivery vehicle (Raspberry Pi Pico).

## Files

| File | Purpose |
|------|---------|
| `config.py` | Pin assignments and tuning constants |
| `motor_driver.py` | L298N dual motor control (PWM) |
| `ultrasonic_sensor.py` | Three HC-SR04 distance sensors |
| `line_detector.py` | Line-following sensor input |
| `ir_payload_detection.py` | Bench test: IR ADC + reed switch |
| `drive_forward_test.py` | Bench test: drive ~4 ft forward |
| `payload_bonus.py` | Payload pickup/drop-off with stepper lift |
| `main.py` | Integrated navigation + payload handling |
| `main_line_trace_draft.py` | Earlier obstacle/line-trace draft (reference) |

## External dependencies (copy to Pico)

- `hcsr04.py` — HC-SR04 ultrasonic driver
- `stepper.py` — half-step stepper motor driver

## Upload and run

1. Copy all `.py` files plus `hcsr04.py` and `stepper.py` to the Pico.
2. Run a test script (e.g. `ir_payload_detection.py`) or `main.py` for full behaviour.
3. Tune speeds, distances, and stepper heights in `config.py` on hardware.

## Fixes applied from original drafts

- Removed duplicate `led` pin assignment in IR test
- Enabled PWM speed control in motor driver (was commented out in early tests)
- Fixed invalid imports (`from module import func()` → proper module imports)
- Fixed missing colons, `i==-1` vs `i=-1`, and undefined `sense_val` / `reverse_speed`
- Resolved line-sensor vs ultrasonic echo pin conflict (line on GPIO 0)
- Centralized pin map in `config.py` for easier tuning
