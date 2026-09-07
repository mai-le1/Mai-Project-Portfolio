# Portable Garden — MicroPython firmware (Raspberry Pi Pico)

Firmware extracted from the group logbook
[`documentation/portable_garden_Logbook.pdf`](../documentation/portable_garden_Logbook.pdf).

## Files

| File | Source in logbook | Purpose |
|------|-------------------|---------|
| `main.py` | Feb 21 — finalized | Production loop: LDR, grow lights, STEMMA soil sensor, pump |
| `main_feb10_draft.py` | Feb 10 — ALT CODE | Earlier integrated draft with LDR + watering |

## Hardware pins

| Function | GPIO | Notes |
|----------|------|-------|
| Soil sensor SDA | 4 | I2C0 |
| Soil sensor SCL | 5 | I2C0 |
| Grow lights | 15 | Transistor base |
| Water pump | 16 | Transistor base; pump on 5 V with series potentiometer for flow |
| Photoresistor (LDR) | 28 | ADC |

## External libraries (copy to Pico)

- `stemma_soil_sensor.py`
- `seesaw.py` (STEMMA / Seesaw dependency)

## Behaviour summary (`main.py`)

- Reads LDR; if darker than `LDR_MAX` (45000), turns grow lights on for up to 4 hours per 24-hour window.
- Reads STEMMA moisture; if ≤ 450 (very dry), runs pump for 3 seconds.
- If moisture is optimal or only moderately dry, pump stays off and the loop delays ~100 s.
- Prints moisture, temperature (°C), LDR value, and status messages.

Moisture guide from logbook / datasheet notes: ~200 very dry → ~2000 very wet; examples Wet ≈ 1015, Dry ≈ 331.

## Upload and run

1. Flash MicroPython on the Raspberry Pi Pico.
2. Copy `main.py`, `stemma_soil_sensor.py`, and `seesaw.py` to the Pico.
3. Reset or run `main.py`.

## Logbook timeline (software)

| Date | Notes |
|------|-------|
| Feb 7 | Materials, pin map, spinach research, first pump/light/soil sketches |
| Feb 10 | Added photoresistor; combined light + soil + pump |
| Feb 13 | Bench-tested code; material/dimension discussion |
| Feb 21 | Finalized code with revised comments; assembled components |
| Feb 25–26 | Assembly, presentation; project finished |
