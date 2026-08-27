"""
Payload pickup and drop-off test (Raspberry Pi Pico).

Focused test for reed-switch payload detection and stepper lift sequencing.
Uses step_until() for position-based lift moves.

Required on Pico filesystem:
  - config.py, motor_driver.py, line_detector.py
  - hcsr04.py, stepper.py
"""

from machine import Pin
from time import sleep

import stepper

import motor_driver
from config import (
    DRIVE_SPEED,
    HEIGHT_LIFT,
    HEIGHT_PICKUP,
    REED_SWITCH_PIN,
    STEPPER_IN1,
    STEPPER_IN2,
    STEPPER_IN3,
    STEPPER_IN4,
    TURN_SPEED,
)

reed_switch = Pin(REED_SWITCH_PIN, Pin.IN, Pin.PULL_DOWN)

stepper_motor = stepper.HalfStepMotor.frompins(
    STEPPER_IN1, STEPPER_IN2, STEPPER_IN3, STEPPER_IN4
)

R_TURN_TIME = 0.485
L_TURN_TIME = 0.495


def drop_off():
    print("lowering lift")
    stepper_motor.step_until(HEIGHT_LIFT - 25, dir=-1)

    print("reverse")
    motor_driver.reverse(DRIVE_SPEED, 3)

    print("reset lift")
    stepper_motor.reset()


def pick_up():
    if reed_switch.value() != 1:
        print("No payload — obstacle or false trigger")
        return False

    print("Payload detected!")
    print("reverse")
    motor_driver.reverse(DRIVE_SPEED, 0.3)

    print("raising lift")
    stepper_motor.step_until(HEIGHT_LIFT, dir=1)

    print("forward")
    motor_driver.drive(DRIVE_SPEED, 3)

    print("moving lift")
    stepper_motor.step_until(HEIGHT_PICKUP, dir=1)

    print("turning")
    return True


def main():
    while True:
        stepper_motor.reset()
        print("Reed switch:", reed_switch.value())

        if reed_switch.value() == 1:
            if pick_up():
                motor_driver.drive(DRIVE_SPEED, 5)
                drop_off()
                motor_driver.drive(DRIVE_SPEED, 1)
                print("done")
                break
        else:
            print("Not found, driving")
            motor_driver.drive(DRIVE_SPEED, 0.3)

        sleep(0.1)


if __name__ == "__main__":
    main()
