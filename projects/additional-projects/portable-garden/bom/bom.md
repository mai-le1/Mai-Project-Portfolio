# Portable Garden — bill of materials

From group logbook (February 7 materials list and later prototype notes).

| Subsystem | Parts / materials | Notes |
|-----------|-------------------|-------|
| Showerhead / irrigation head | 3D printed | |
| Plant holder | Pipe or water bottles, coffee filters | Feb 14 prototype: bottle 225 mm |
| Enclosure | LEDs, polyethylene base, 3D-printed walls and roof | Early estimate ~4.5×4.5×10 in (114.3×114.3×254 mm); Feb 14 box 145 mm |
| Electronics housing | Breadboard, wiring | Connections for soil and light sensors |
| Soil sensing | Adafruit STEMMA soil sensor (Seesaw) | I2C GPIO 4 / 5 |
| Light sensing | Photoresistor (LDR) | ADC GPIO 28 |
| Grow lighting | Grow LEDs + drive transistor | GPIO 15 to transistor base |
| Watering | Pump, tubing, drive transistor, potentiometer | GPIO 16; pump on Pico 5 V with series pot for flow |
| Controller | Raspberry Pi Pico | MicroPython |

Update part numbers / quantities when purchasing records are available.
