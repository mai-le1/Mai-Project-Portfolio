"""
Portable Garden — earlier integrated draft (February 10 logbook).

Includes photoresistor (LDR) logic with grow lights and soil/pump control.
Kept for reference; prefer main.py (February 21 finalized version).

Note: original logbook used `machine.ADC(28)` without `import machine`.
This file uses `ADC(28)` after importing ADC from machine.
"""

from machine import Pin, I2C, ADC
import time
from stemma_soil_sensor import StemmaSoilSensor

SDA_PIN = 4
SCL_PIN = 5
grow_lights = Pin(15, Pin.OUT)
pump = Pin(16, Pin.OUT)
ldr = ADC(28)

i2c = I2C(0, sda=Pin(SDA_PIN), scl=Pin(SCL_PIN), freq=400000)
stemma_soil_sensor = StemmaSoilSensor(i2c)
seesaw = stemma_soil_sensor

ldr_min = 1  # NOTE: initialize later from measured photoresistor values

time_initial = time.time()
time_on = 0
grow_lights_on = False


def soil_moisture():
    try:
        moisture = seesaw.get_moisture()
        temperature = seesaw.get_temp()
        print(f"Moisture Level: {moisture}, Temperature: {temperature:.1f}°C")

        soil_m_optimal = True
        soil_m_vdry = False

        if moisture <= 950:
            soil_m_optimal = False
            if moisture <= 450:
                soil_m_vdry = True

        if soil_m_optimal:
            return 1
        elif soil_m_vdry:
            return 2
        else:
            return 3

    except Exception as e:
        print(f"Error,Resetting: {e}")
        time.sleep(10)
        global i2c, stemma_soil_sensor, seesaw
        i2c = I2C(0, sda=Pin(SDA_PIN), scl=Pin(SCL_PIN), freq=400000)
        stemma_soil_sensor = StemmaSoilSensor(i2c)
        seesaw = stemma_soil_sensor
        return 0


while True:
    ldr_value = ldr.read_u16()
    print("LDR Value:", ldr_value)

    if (time.time() - time_initial) >= 86400:
        time_initial = time.time()
        time_on = 0

    if ldr_value < ldr_min and grow_lights_on is False:
        grow_lights.value(1)
        time_on = time.time()
        grow_lights_on = True
        print("Light status: dark. Turned lights on.")

    if ((time.time() - time_on) >= 14400) and grow_lights_on is True:
        grow_lights.value(0)
        grow_lights_on = False
        print("4 hours of light elapsed. Turned lights off.")

    water = soil_moisture()

    if water == 1:
        pump.value(0)
        time.sleep(100)
        print("Moisture status: optimal.")
    elif water == 2:
        pump.value(1)
        time.sleep(3)
        pump.value(0)
        print("Moisture status: very dry. Watered.")
    elif water == 3:
        pump.value(0)
        time.sleep(100)
        print("Moisture status: dry. Will water later.")
    else:
        print("Error in soil sensor.")
