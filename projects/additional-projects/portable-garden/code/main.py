"""
Portable Garden — Raspberry Pi Pico (MicroPython) firmware

Finalized version from group logbook (February 21).

Controls:
  - Adafruit STEMMA soil sensor (I2C) for moisture + temperature
  - LDR photoresistor (ADC) for ambient light
  - Grow lights via transistor (GPIO 15)
  - Water pump via transistor (GPIO 16)

Libraries required on the Pico:
  - stemma_soil_sensor.py
  - seesaw.py (dependency of STEMMA soil sensor)
"""

from machine import Pin, I2C, ADC
import time
from stemma_soil_sensor import StemmaSoilSensor

# Pin definitions
SDA_PIN = 4  # GPIO 4
SCL_PIN = 5  # GPIO 5
grow_lights = Pin(15, Pin.OUT)  # Grow lights: transistor base on GPIO 15
pump = Pin(16, Pin.OUT)  # Pump: transistor base on GPIO 16
ldr = ADC(28)  # LDR on ADC pin 28

i2c = I2C(0, sda=Pin(SDA_PIN), scl=Pin(SCL_PIN), freq=400000)
stemma_soil_sensor = StemmaSoilSensor(i2c)
seesaw = stemma_soil_sensor

# Thresholds / timing (seconds)
LDR_MAX = 45000  # darkness threshold (higher LDR reading => darker)
DAY_DURATION = 86400  # 24 hours
GROW_LIGHT_DURATION = 14400  # 4 hours of supplemental light per day

time_initial = time.time()  # start of 24-hour cycle
time_on = 0  # time when grow lights were turned on
grow_lights_on = False


def soil_moisture(moisture):
    """
    Classify soil moisture from STEMMA reading.
    Datasheet range ~200 (very dry) to ~2000 (very wet).
    Returns: 1=optimal, 2=very dry, 3=dry, 0=error
    """
    try:
        soil_m_optimal = True
        soil_m_vdry = False

        if moisture <= 950:
            soil_m_optimal = False  # dry
            if moisture <= 450:
                soil_m_vdry = True  # very dry

        if soil_m_optimal:
            return 1
        elif soil_m_vdry:
            return 2
        else:
            return 3

    except Exception as e:
        print(f"Error, Resetting: {e}")
        time.sleep(10)
        global i2c, stemma_soil_sensor, seesaw
        i2c = I2C(0, sda=Pin(SDA_PIN), scl=Pin(SCL_PIN), freq=400000)
        stemma_soil_sensor = StemmaSoilSensor(i2c)
        seesaw = stemma_soil_sensor
        return 0


while True:
    ldr_value = ldr.read_u16()
    print("LDR Value:", ldr_value)

    moisture = seesaw.get_moisture()
    temperature = seesaw.get_temp()
    print(f"Moisture Level: {moisture}, Temperature: {temperature:.1f}°C")

    # Reset daily light budget every 24 hours
    if (time.time() - time_initial) >= DAY_DURATION:
        time_initial = time.time()
        time_on = 0

    if ldr_value > LDR_MAX and not grow_lights_on:
        grow_lights.value(1)
        time_on = time.time()
        grow_lights_on = True
        print("Light status: dark. Turned lights on.")

    if (time.time() - time_on) >= GROW_LIGHT_DURATION and grow_lights_on:
        grow_lights.value(0)
        grow_lights_on = False
        print("4 hours of light elapsed. Turned lights off.")

    water_status = soil_moisture(moisture)

    if water_status == 1:  # optimal
        pump.value(0)
        time.sleep(100)
        print("Moisture status: optimal.")

    elif water_status == 2:  # very dry
        pump.value(1)
        time.sleep(3)
        pump.value(0)
        print("Moisture status: very dry. Watered.")

    elif water_status == 3:  # dry but not very dry
        pump.value(0)
        time.sleep(100)
        print("Moisture status: dry. Will water later.")

    else:
        print("Error in soil sensor.")

    time.sleep(1)
