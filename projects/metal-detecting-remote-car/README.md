# Remote-Controlled Metal Detection Vehicle

A vintage-style remote-controlled car with rack-and-pinion steering, a differential rear-drive system, ultrasonic distance sensing, and continuity-based metal detection. Built for **ENEL 300 (Winter 2026)** as Team 2.

**Category:** Embedded Systems / Sensing  
**Status:** Completed  
**Course:** ENEL 300 – Winter 2026  
**Team:** Divy Tiwari, Rodrigo Hernandez, Isabella Huber, **Mai Le**, Atharva Mohandas  
**Instructor:** Phillipe Gray

---

## Hero image

![Assembled car with cover](images/car-cover-assembled.png)

---

## Overview

The goal was to build a remote-controlled car that feels more realistic than a typical dual-motor RC toy. Instead of skid steering, the vehicle uses **rack-and-pinion front steering**, a **differential rear-wheel drive system**, and a **steering-wheel-style remote** with potentiometers and drive buttons.

The design pivoted from an initial Formula One concept to a **classic luxury off-road vehicle** inspired by 1930s–1940s cars, combining modern embedded control with a vintage mechanical aesthetic.

Key systems:

- **Dual ESP32** boards communicating over **ESP-NOW** (driver remote + car receiver)
- **HC-SR04** ultrasonic sensor with distance shown on an **I2C LCD**
- **Continuity-based metal detector** with probe wires under the chassis
- **Custom KiCad PCB** integrating power, motor driver, buck converter, fuse protection, and sensing
- **3D-printed mechanical assemblies** — chassis, differential, steering, enclosures, and remote housing

---

## Project status

| Milestone | Status | Notes |
|-----------|--------|-------|
| Electrical schematic & PCB | Done | Custom 80×100 mm 2-layer board |
| Dual ESP32 firmware | Done | ESP-NOW driver/receiver with dual-core tasks |
| Mechanical CAD & 3D printing | Done | SolidWorks assemblies with tolerance tuning |
| Metal detection | Done | Pivoted from NE555 coil to continuity method |
| Ramp climb test (~21°) | Done | Successful with reduced speed under load |
| Final report | Done | [documentation/ENEL_300_W26_TEAM02_Final_Report.pdf](documentation/ENEL_300_W26_TEAM02_Final_Report.pdf) |

---

## My role

Team project (5 members) — I **owned the electrical systems** for the vehicle.

- Designed and built the full electrical architecture: power distribution, motor drive, buck converter, fuse protection, ultrasonic sensor interface, metal-detector circuit, and ESP32 integration.
- **Designed and laid out the custom KiCad PCB** (80×100 mm, 2-layer), including thermal-aware trace widths, ground pour, and connector placement for the motor, battery, servo, and sensors.
- Implemented the metal-detection subsystem, including the pivot from an unreliable NE555 coil design to continuity-based probing.
- Brought up and debugged hardware on the custom board (12 V motor rail, 5 V control supply, 3.3 V LDO for headlights).

Teammates contributed mechanical CAD, firmware, and integration/testing. See the [final report](documentation/ENEL_300_W26_TEAM02_Final_Report.pdf) for full team documentation.

---

## Features

### Implemented

- Rack-and-pinion front steering with servo control and ball-bearing mounts
- Differential rear-wheel drive with 3D-printed crown and side gears
- Dual ESP32 ESP-NOW wireless link (steering wheel + pedal remote → car receiver)
- HC-SR04 front distance sensing displayed on I2C LCD
- Continuity-based metal detection with buzzer alert
- Custom PCB with 12 V motor supply, 5 V buck converter, 3.3 V LDO, and 5 A fuse protection
- Vintage-style car enclosure and custom steering-wheel / button remote housings

### Known limitations

- Reduced speed and minor steering instability when climbing inclines under load
- Original NE555 coil metal detector was unreliable and replaced with continuity detection

---

## Hardware

| Component | Purpose | Notes |
|-----------|---------|-------|
| ESP32 (×2) | Driver remote + car receiver | ESP-NOW communication |
| HC-SR04 | Front distance sensing | Echo/trig on GPIO 26/25 |
| 12 V 200 RPM geared DC motor | Propulsion | Rear differential drive |
| 12.6 V Li-Ion battery | Motor power | 5 A BMS output limit |
| Servo motor | Rack-and-pinion steering | Replaced initial stepper design |
| H-bridge motor driver | DC motor control | PWM forward/reverse/stop |
| Buck converter IC | 12 V → 5 V | Powers ESP32 and logic |
| LDO | 5 V → 3.3 V | Headlight supply |
| 5 A fuse | Motor protection | Isolates stall from control electronics |
| LCD display | Distance readout | I2C (HD44780-compatible) |
| Potentiometers (×2) | Steering + throttle | On driver remote |
| Buttons (×2) | Forward / reverse | On driver remote |
| Metal detector | Continuity probe | Two wires under chassis |

---

## Software

- **Language / toolchain:** C on ESP32 (VS Code + Espressif IDE)
- **Protocol:** ESP-NOW peer-to-peer between driver and receiver ESP32
- **Driver MCU:** Reads potentiometers/buttons, drives I2C LCD, sends control data
- **Receiver MCU:** Motor PWM, servo steering, ultrasonic ranging, metal detection
- **Dual-core scheduling:** Driving/receive on core 0; ultrasonic + servo tasks on core 1

### Architecture

**Driver (remote):**

![Driver architecture](documentation/driver-architecture.png)

**Receiver (car):**

![Receiver architecture](documentation/receiver-architecture.png)

Key receiver functions: `receive_callback`, `servo_task`, `motor_forward/reverse/stop`, `get_distance`, `ultrasonic_task`, `send_distance`.

Key driver functions: ESP-NOW send/receive callbacks, I2C LCD helpers (`lcd_init`, `lcd_print_line`), ADC reads for potentiometers.

---

## Design tools

- **KiCad** — schematics and custom PCB layout
- **SolidWorks** — chassis, differential, steering, enclosures, remote housings
- **Lucidchart** — software architecture diagrams

---

## System architecture

```text
Driver ESP32 ──ESP-NOW──► Receiver ESP32
     │                          │
  Potentiometers              Servo (steering)
  Buttons                     Motor driver (drive)
  I2C LCD ◄── distance ──    HC-SR04 ultrasonic
                              Metal detector (continuity)
```

### Electrical block diagram

![Electrical block diagram](schematics/electrical-block-diagram.png)

---

## Electrical design

### Metal detector circuit

An initial NE555 oscillator + coil design proved unreliable. The team pivoted to **continuity detection**: two probe wires under the car close the circuit when contacting a metal plate, sounding a buzzer.

![Metal detector circuit](schematics/metal-detector-circuit.png)

### Motor drive circuit

![Motor drive schematic](schematics/motor-drive-circuit.png)

### Power management

- **12 V** motor and battery rail with **5 A fuse** in series (stall protection; control electronics stay powered)
- Estimated motor current: ~0.7 A no-load, ~1.39 A on 20° incline, up to 12.6 A stall
- **5 V** buck converter for ESP32; **3.3 V** LDO for headlights

### Custom PCB

![Custom PCB design](pcb/custom-pcb-design.png)

- 80×100 mm, 2-layer board with copper ground pour and thermal-aware trace widths
- Integrates fuse, buck converter, motor driver, ESP32 headers, ultrasonic connector, and metal-detector circuit
- Widest traces (2.0 mm) on battery-to-fuse path

- Schematics: see [schematics/](schematics/)
- PCB: see [pcb/](pcb/)
- BOM: see [bom/](bom/) and final report Appendix A

---

## Mechanical design

### Rack-and-pinion steering

![Rack and pinion steering](cad/rack-and-pinion-steering.png)

![Steering integrated in chassis](cad/steering-chassis-integration.png)

Four 11 mm and two 23 mm ball bearings for smooth steering and wheel rotation.

### Chassis and differential

![Chassis angled view](cad/chassis-angled-view.png)

![Differential system](cad/differential-system.png)

![Differential mounted](cad/differential-mounted.png)

The differential uses a crown gear driving parallel differential gears for realistic rear-wheel speed difference. Four rear ball bearings were added after the first sprint when the differential contacted the ground.

### Car floor, PCB mount, and metal probes

![Car floor with battery and motor](cad/car-floor-battery-motor.png)

![Fully assembled floor in chassis](cad/floor-assembled-chassis.png)

![Metal detection cable holder](cad/metal-detection-cable-holder.png)

### Enclosures

![Car front](images/car-front-enclosure.png)

![Car back](images/car-back-enclosure.png)

![Car cover assembled](images/car-cover-assembled.png)

### Remote control housing

![Steering wheel assembly](images/steering-wheel-assembly.png)

![Button enclosure](images/button-enclosure.png)

---

## Challenges and debugging

### Issue: NE555 coil metal detector unreliable

- **Problem:** Oscillator frequency shift from nearby metal was too small to detect reliably.
- **Expected behaviour:** Buzzer frequency would change noticeably near metal objects.
- **What failed:** Potentiometer and transistor tuning did not improve sensitivity enough.
- **What changed:** Replaced with continuity-based detection using two probe wires under the chassis.
- **What was learned:** Simpler contact-based sensing can be more reliable than inductive detection for a ground-level metal plate task.

### Issue: Differential ground contact on first sprint

- **Problem:** Rear differential dragged on the ground during operation.
- **What changed:** Added four ball bearings to support rear wheels and keep the differential elevated.
- **What was learned:** Mechanical tolerances and bearing support must be validated early in drive testing.

### Issue: Steering motor selection

- **Problem:** Stepper motor steering left unused PCB pins and was replaced.
- **What changed:** Switched to a servo motor for rack-and-pinion angle control with PWM duty mapping.

---

## Testing and results

| Test | Method | Result |
|------|--------|--------|
| Flat-ground driving | Remote steering + forward/reverse | Smooth motion |
| Incline climb (~21°) | Ramp test with ~0.9 kg vehicle | Successful climb; reduced speed under load |
| Ultrasonic distance | HC-SR04 → LCD display | Distance shown on driver LCD |
| Metal detection | Continuity probes on metal plate | Buzzer sounds on contact |
| Motor stall protection | 5 A fuse in motor line | Control electronics remain powered |

Full test notes and BOM: [documentation/ENEL_300_W26_TEAM02_Final_Report.pdf](documentation/ENEL_300_W26_TEAM02_Final_Report.pdf)

---

## Repository structure

```text
metal-detecting-remote-car/
├── README.md
├── code/              # Firmware (see final report Appendix B)
├── schematics/        # Block diagram, metal detector, motor drive
├── pcb/               # Custom PCB layout
├── cad/               # SolidWorks / 3D-printed part renders
├── documentation/     # Final report and architecture diagrams
├── images/            # Enclosure and remote photos
├── videos/            # Demo clips
├── bom/               # Bill of materials
└── test-results/      # Test logs
```

---

## Future improvements

- Higher-torque motor or higher-voltage drive for faster incline climbing
- Stronger servo or alternate steering mechanism for stability on ramps
- Restore inductive metal detection with improved coil/circuit design
- Add autonomous navigation modes beyond manual remote control

---

## Safety and limitations

- 12 V Li-Ion battery — follow charging and storage guidelines
- 5 A fuse protects against motor stall overcurrent; replace if blown
- Metal detector uses exposed probe wires — avoid shorting against unintended conductors
- Reduced steering stability on inclines; not designed for high-speed operation

---

## Acknowledgements

- ENEL 300 course staff and Makerspace (LCD provided)
- Team members: Divy Tiwari, Rodrigo Hernandez, Isabella Huber, Mai Le, Atharva Mohandas

---

## References

See [documentation/ENEL_300_W26_TEAM02_Final_Report.pdf](documentation/ENEL_300_W26_TEAM02_Final_Report.pdf) for full references (HD44780 LCD datasheet, motor driver module, geared DC motor).

---

## License

Course project — rights reserved unless otherwise specified by the team.
