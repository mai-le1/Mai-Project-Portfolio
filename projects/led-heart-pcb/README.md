# Heartbeat LED PCB

A custom 5 V heartbeat LED PCB designed in KiCad using an ATtiny1616 microcontroller, two daisy-chained 74HC595 shift registers, and 16 individually controlled LEDs. The firmware is written in C and generates synchronized heartbeat-style lighting patterns.

**Category:** PCB Design / Electronics  
**Status:** Completed

---

## Hero image

<!-- Add a photo of the assembled board to images/ and link it here.
     Example: ![Assembled heart PCB](images/hero.jpg) -->

> **Image placeholder:** Add a hero photo, prototype shot, or assembled board image to `images/` and link it here.

---

## Overview

The circuit is divided into four main sections: power and protection, ATtiny1616 control, 74HC595 LED expansion, and the LED output stage. An external 5 V supply powers the board through reverse-polarity protection and an on/off switch. The ATtiny1616 drives two daisy-chained shift registers with only three GPIO pins, expanding to 16 independently controlled LEDs arranged around the perimeter of a heart-shaped PCB.

The firmware sends 16-bit LED patterns to the shift registers and uses software PWM to create a realistic heartbeat animation — a strong first pulse, a weaker second pulse, and a longer resting interval.

---

## System architecture

```text
5V Input → Protection & Power → ATtiny1616
                                  │
                           DATA / CLK / LATCH
                                  │
                                  ▼
                         2× 74HC595
                                  │
                           16 Outputs
                                  │
                                  ▼
                              16 LEDs
```

---

## Project status

| Milestone | Status | Notes |
|-----------|--------|-------|
| Schematic design | Done | Power, MCU, shift registers, LED outputs |
| PCB layout | Done | Heart-shaped board in KiCad |
| Firmware | Done | Shift-register driver and heartbeat animation |
| Assembly and test | TODO | Add notes once board is built and verified |

---

## My role

Personal project — I designed the schematic and PCB in KiCad and wrote the ATtiny1616 firmware in C.

- Designed the 5 V power path with reverse-polarity protection and decoupling.
- Selected and integrated ATtiny1616 with UPDI programming header.
- Daisy-chained two 74HC595 shift registers to control 16 LEDs from 3 GPIO pins.
- Wrote C firmware for shift-register communication, software PWM, and heartbeat animation.

---

## Features

### Implemented

- Custom heart-shaped PCB with 16 individually addressable LEDs.
- ATtiny1616 microcontroller with UPDI in-system programming.
- Two daisy-chained 74HC595 shift registers (3 GPIO pins → 16 outputs).
- SS14 Schottky diode for reverse-polarity protection and slide on/off switch.
- Software PWM brightness control for smooth heartbeat animation.
- Synchronized double-pulse heartbeat pattern (strong beat, weaker beat, rest).

### Planned

- Add assembled board photos and test results after fabrication.

---

## Hardware

### 1. Power and protection

The board receives an external 5 V supply through a 2-pin connector.

Power path:

```text
5V Input → SS14 Schottky Diode → ON/OFF Switch → VCC
```

The SS14 diode provides reverse-polarity protection, while the slide switch allows the board to be turned on and off without disconnecting the power source.

A 10 µF bulk capacitor helps stabilize the supply during changes in LED current, while 0.1 µF decoupling capacitors are placed near each digital IC to suppress high-frequency noise.

### 2. ATtiny1616 controller

The ATtiny1616 acts as the brain of the system and runs the heartbeat firmware written in C.

Three GPIO pins control the entire LED array:

| Pin | Signal |
|-----|--------|
| PB0 | DATA |
| PB1 | CLK |
| PB2 | LATCH |

The MCU also includes a UPDI programming interface through PA0, allowing the firmware to be uploaded after the ATtiny is soldered onto the PCB. A 3-pin header exposes VCC, UPDI, and GND.

### 3. 74HC595 LED expansion

Two 74HC595 serial-in/parallel-out shift registers allow the ATtiny to control 16 LEDs using only three GPIO pins.

The ATtiny sends LED states serially through DATA. Each CLK pulse shifts another bit into the registers. After all 16 bits have been loaded, the MCU pulses LATCH, causing all 16 outputs to update simultaneously.

The registers are daisy-chained:

```text
ATtiny DATA → U2 SER
U2 QH' → U3 SER
```

This expands the system from 3 MCU control signals to 16 independently controlled outputs.

### 4. LED output stage

Each shift-register output controls one LED through its own 1 kΩ current-limiting resistor:

```text
74HC595 Output → 1kΩ → LED → GND
```

U2 controls LEDs 1–8 and U3 controls LEDs 9–16. The LEDs are physically arranged around the perimeter of the heart-shaped PCB.

| Component | Purpose | Notes |
|-----------|---------|-------|
| ATtiny1616 | MCU | Heartbeat firmware, shift-register control |
| 74HC595 (×2) | Shift registers | Daisy-chained, 16 parallel outputs |
| SS14 Schottky diode | Reverse-polarity protection | In series with 5 V input |
| Slide switch | Power on/off | Between diode and VCC |
| 1 kΩ resistors (×16) | LED current limiting | One per LED |
| 10 µF capacitor | Bulk decoupling | Supply stabilization |
| 0.1 µF capacitors | IC decoupling | Near each digital IC |

---

## Software

- **Language / toolchain:** C (AVR-GCC) on ATtiny1616
- **Libraries:** avr/io.h, util/delay.h
- **Source:** [code/heartbeatcode.c](code/heartbeatcode.c)
- **Flash / build:** UPDI programmer via 3-pin header (VCC, UPDI, GND)

---

## Design tools

- **KiCad** — schematic capture and heart-shaped PCB layout

---

## Electrical design

- Schematics: see [schematics/](schematics/)
- PCB: see [pcb/](pcb/)
- BOM: see [bom/](bom/)

---

## Firmware

The firmware communicates with the shift registers using a 16-bit LED pattern.

For example:

```c
write_leds(0xFFFF);  // All 16 LEDs ON
write_leds(0x0000);  // All 16 LEDs OFF
write_leds(0x0001);  // One LED ON
```

For every pattern, the ATtiny:

1. Set DATA
2. Pulse CLK × 16
3. Pulse LATCH → LEDs update

The `heartbeat()` function combines timed pulses and PWM-style brightness control to create a strong first pulse, weaker second pulse, and longer resting interval, rather than simply switching the LEDs on and off.

Key functions in [code/heartbeatcode.c](code/heartbeatcode.c):

| Function | Purpose |
|----------|---------|
| `gpio_init()` | Configure PB0–PB2 as outputs |
| `shift_bit()` | Send one bit on DATA and pulse CLK |
| `write_leds()` | Shift 16 bits and latch to outputs |
| `show_brightness()` | Software PWM for variable brightness |
| `fade_up()` / `fade_down()` | Smooth brightness transitions |
| `heartbeat()` | Double-pulse animation loop |

---

## Development process

1. Defined system architecture: MCU → shift registers → 16 LEDs.
2. Designed schematic and heart-shaped PCB layout in KiCad.
3. Wrote and tested firmware for shift-register communication and heartbeat animation.

---

## Challenges and debugging

TODO: Document real debugging stories as they are resolved. Use this structure for each issue:

### Issue: TODO title

- **Problem:** TODO
- **Expected behaviour:** TODO
- **How it was tested:** TODO
- **What failed:** TODO
- **What changed:** TODO
- **What was learned:** TODO

---

## Testing and results

Record test setups and outcomes in [test-results/](test-results/).

| Test | Method | Result | Date |
|------|--------|--------|------|
| Shift-register communication | Bench test with logic analyzer or LED patterns | TODO | TODO |
| Heartbeat animation timing | Visual inspection of double-pulse pattern | TODO | TODO |
| Power-on with reverse polarity | Verify SS14 protection | TODO | TODO |

Photos, logs, and notes belong in test-results/ and images/.

---

## Repository structure

```text
led-heart-pcb/
├── README.md
├── code/              # Firmware and application source
├── schematics/        # Schematic sources and exports
├── pcb/               # PCB layout, Gerbers, fabrication outputs
├── cad/               # Mechanical CAD and 3D models
├── documentation/     # Design notes, reports, write-ups
├── images/            # Photos and diagrams
├── videos/            # Demo clips (prefer links for large files)
├── bom/               # Bill of materials
└── test-results/      # Test logs, tables, and observations
```

---

## Future improvements

- Add assembled board photos and demo video.
- Experiment with alternative LED patterns (breathing, chase, etc.).
- Add a button input for pattern selection.

---

## Safety and limitations

- Operates at 5 V only — do not exceed the rated supply voltage.
- Reverse-polarity protection is provided by the SS14 diode, but always verify polarity before powering on.
- LED current is set by 1 kΩ resistors — do not bypass current-limiting resistors.

---

## Acknowledgements

- KiCad open-source EDA tools.

---

## License

TODO: Choose a license for this project folder (or state that rights are reserved).
