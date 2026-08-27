"""
IR and payload detection test (Raspberry Pi Pico).

Reads an IR ADC sensor and a reed switch. The onboard LED turns on when
the reed switch detects a magnet or when IR reflection exceeds the threshold.

Upload config.py and run this file standalone on the Pico.
"""

from machine import ADC, Pin
from time import sleep

from config import IR_ADC_PIN, IR_THRESHOLD, REED_SWITCH_PIN

reed_switch = Pin(REED_SWITCH_PIN, Pin.IN, Pin.PULL_DOWN)
led = Pin("LED", Pin.OUT)
ir = ADC(IR_ADC_PIN)


def main():
    while True:
        ir_value = ir.read_u16()
        reed_value = reed_switch.value()

        print("IR value:", ir_value)
        print("Reed switch value:", reed_value)

        if reed_value == 1:
            led.value(1)
        elif ir_value > IR_THRESHOLD:
            print("IR detected")
            led.value(1)
        else:
            led.value(0)

        sleep(1)


if __name__ == "__main__":
    main()
