"""
Main autonomous navigation loop (Raspberry Pi Pico).

Combines ultrasonic obstacle avoidance, line re-acquisition, and payload
pickup/drop-off using a stepper-driven lift.

Required on Pico filesystem:
  - config.py, motor_driver.py, ultrasonic_sensor.py, line_detector.py
  - hcsr04.py (HC-SR04 driver)
  - stepper.py (half-step stepper driver)

This is a cleaned-up version of the integrated "bonus tests" firmware.
"""

from machine import Pin
from time import sleep

import stepper
from hcsr04 import HCSR04

import line_detector
import motor_driver
from config import (
    BUTTON_PIN,
    DRIVE_SPEED,
    DRIVE_TIME,
    HEIGHT_DRIVE,
    HEIGHT_LIFT,
    HEIGHT_PICKUP,
    OBSTACLE_DISTANCE_CM,
    PAYLOAD_DISTANCE_CM,
    REED_SWITCH_PIN,
    STEPPER_IN1,
    STEPPER_IN2,
    STEPPER_IN3,
    STEPPER_IN4,
    TURN_SPEED,
    TURN_TIME,
    ULTRASONIC_FRONT,
    ULTRASONIC_LEFT,
    ULTRASONIC_RIGHT,
)

reed_switch = Pin(REED_SWITCH_PIN, Pin.IN, Pin.PULL_DOWN)
button = Pin(BUTTON_PIN, Pin.IN, Pin.PULL_DOWN)

stepper_motor = stepper.HalfStepMotor.frompins(
    STEPPER_IN1, STEPPER_IN2, STEPPER_IN3, STEPPER_IN4
)
stepper_motor.reset()

sensor_front = HCSR04(
    trigger_pin=ULTRASONIC_FRONT[0], echo_pin=ULTRASONIC_FRONT[1]
)
sensor_right = HCSR04(
    trigger_pin=ULTRASONIC_RIGHT[0], echo_pin=ULTRASONIC_RIGHT[1]
)
sensor_left = HCSR04(
    trigger_pin=ULTRASONIC_LEFT[0], echo_pin=ULTRASONIC_LEFT[1]
)


def pick_up():
    """Reverse, raise lift, drive forward to capture payload, lift off ground."""
    if reed_switch.value() != 1:
        return False

    print("Payload detected!")
    motor_driver.reverse(TURN_SPEED, 0.5)
    stepper_motor.step(HEIGHT_PICKUP)

    # Drive until operator presses button (or replace with line/autonomous logic)
    while button.value() != 1:
        motor_driver.motor_a("forward", DRIVE_SPEED)
        motor_driver.motor_b("forward", DRIVE_SPEED)
    motor_driver.stop()

    stepper_motor.step(500)
    motor_driver.right_turn(TURN_SPEED, TURN_TIME)
    motor_driver.right_turn(TURN_SPEED, TURN_TIME)
    return True


def drop_off():
    """Lower lift, reverse clear of payload zone, reset stepper position."""
    stepper_motor.step(-1 * HEIGHT_LIFT)
    motor_driver.reverse(TURN_SPEED, 1.0)
    stepper_motor.step(HEIGHT_DRIVE)


def back_to_line(direction="right"):
    """Re-find the line after passing a side obstacle."""
    while True:
        if direction == "right":
            motor_driver.right_turn(TURN_SPEED, TURN_TIME)
            if line_detector.sensor_val() == 1:
                motor_driver.drive(DRIVE_SPEED, DRIVE_TIME)
            if line_detector.sensor_val() == 0:
                motor_driver.left_turn(TURN_SPEED, TURN_TIME)
                break
        elif direction == "left":
            motor_driver.left_turn(TURN_SPEED, TURN_TIME)
            if line_detector.sensor_val() == 1:
                motor_driver.drive(DRIVE_SPEED, DRIVE_TIME)
            if line_detector.sensor_val() == 0:
                motor_driver.right_turn(TURN_SPEED, TURN_TIME)
                break

        d1 = sensor_front.distance_cm()
        d2 = sensor_right.distance_cm()
        d3 = sensor_left.distance_cm()
        if (
            d1 <= OBSTACLE_DISTANCE_CM
            or d2 <= OBSTACLE_DISTANCE_CM
            or d3 <= OBSTACLE_DISTANCE_CM
        ):
            break


def main():
    while True:
        distance_front = sensor_front.distance_cm()
        distance_right = sensor_right.distance_cm()
        distance_left = sensor_left.distance_cm()

        print(
            "Distances - Front: {}cm, Right: {}cm, Left: {}cm".format(
                distance_front, distance_right, distance_left
            )
        )

        # Payload detection and handling
        if reed_switch.value() == 1 and distance_front <= PAYLOAD_DISTANCE_CM:
            if pick_up():
                motor_driver.drive(DRIVE_SPEED, 3)
                drop_off()
                motor_driver.drive(DRIVE_SPEED, 3)
                motor_driver.right_turn(TURN_SPEED, TURN_TIME)
                motor_driver.right_turn(TURN_SPEED, TURN_TIME)

        # Obstacle handling
        elif distance_front <= OBSTACLE_DISTANCE_CM and distance_front > 0:
            motor_driver.right_turn(TURN_SPEED, TURN_TIME)

        elif distance_right <= OBSTACLE_DISTANCE_CM and distance_right > 0:
            while distance_right <= OBSTACLE_DISTANCE_CM:
                motor_driver.drive(DRIVE_SPEED, 0.5)
                distance_right = sensor_right.distance_cm()
            back_to_line("right")

        elif distance_left <= OBSTACLE_DISTANCE_CM and distance_left > 0:
            while distance_left <= OBSTACLE_DISTANCE_CM:
                motor_driver.drive(DRIVE_SPEED, 0.5)
                distance_left = sensor_left.distance_cm()
            back_to_line("left")

        else:
            motor_driver.drive(DRIVE_SPEED, DRIVE_TIME)

        sleep(0.1)


if __name__ == "__main__":
    main()
