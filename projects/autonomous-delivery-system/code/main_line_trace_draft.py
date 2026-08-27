"""
Early line-tracing + obstacle avoidance draft.

This was the original integrated main loop before the bonus tests version.
Kept for reference — several syntax and logic issues from the original
have been fixed below. Use main.py for the integrated vehicle firmware.
"""

from time import sleep

import line_detector
import motor_driver
import ultrasonic_sensor
from config import DRIVE_SPEED, DRIVE_TIME, OBSTACLE_DISTANCE_CM, TURN_SPEED, TURN_TIME

distance_1 = ultrasonic_sensor.distance1
distance_2 = ultrasonic_sensor.distance2
distance_3 = ultrasonic_sensor.distance3
sensor_val = line_detector.sensor_val
right = motor_driver.right_turn
left = motor_driver.left_turn
straight = motor_driver.drive
back = motor_driver.reverse


def back_to_line(direction="right"):
    """Re-acquire the line after clearing a side obstacle."""
    if direction == "right":
        while direction == "right":
            right(TURN_SPEED, TURN_TIME)

            if sensor_val() == 1:
                straight(DRIVE_SPEED, DRIVE_TIME)

            if sensor_val() == 0:
                left(TURN_SPEED, TURN_TIME)
                break

            if (
                distance_1() <= OBSTACLE_DISTANCE_CM
                or distance_2() <= OBSTACLE_DISTANCE_CM
                or distance_3() <= OBSTACLE_DISTANCE_CM
            ):
                break

    elif direction == "left":
        while direction == "left":
            left(TURN_SPEED, TURN_TIME)

            if sensor_val() == 1:
                straight(DRIVE_SPEED, DRIVE_TIME)

            if sensor_val() == 0:
                right(TURN_SPEED, TURN_TIME)
                break

            if (
                distance_1() <= OBSTACLE_DISTANCE_CM
                or distance_2() <= OBSTACLE_DISTANCE_CM
                or distance_3() <= OBSTACLE_DISTANCE_CM
            ):
                break


def main():
    while True:
        d1 = distance_1()
        d2 = distance_2()
        d3 = distance_3()

        if d1 <= OBSTACLE_DISTANCE_CM:
            right(TURN_SPEED, TURN_TIME)

        elif d1 <= OBSTACLE_DISTANCE_CM and d2 >= OBSTACLE_DISTANCE_CM:
            left(TURN_SPEED, TURN_TIME)

        elif d1 <= OBSTACLE_DISTANCE_CM and d3 >= OBSTACLE_DISTANCE_CM:
            right(TURN_SPEED, TURN_TIME)

        elif d2 <= OBSTACLE_DISTANCE_CM:
            while d2 <= OBSTACLE_DISTANCE_CM:
                straight(DRIVE_SPEED, DRIVE_TIME)
                d2 = distance_2()
            back_to_line("right")

        elif d3 <= OBSTACLE_DISTANCE_CM:
            while d3 <= OBSTACLE_DISTANCE_CM:
                straight(DRIVE_SPEED, DRIVE_TIME)
                d3 = distance_3()
            back_to_line("left")

        elif d3 <= OBSTACLE_DISTANCE_CM and d2 >= OBSTACLE_DISTANCE_CM:
            straight(DRIVE_SPEED, DRIVE_TIME)

        elif (
            d1 >= OBSTACLE_DISTANCE_CM
            and d2 >= OBSTACLE_DISTANCE_CM
            and d3 >= OBSTACLE_DISTANCE_CM
        ):
            while True:
                if d2 >= OBSTACLE_DISTANCE_CM and d3 >= OBSTACLE_DISTANCE_CM:
                    right(TURN_SPEED, TURN_TIME)
                    straight(DRIVE_SPEED, DRIVE_TIME)
                    break
                else:
                    back(TURN_SPEED, TURN_TIME)
                d1 = distance_1()
                d2 = distance_2()
                d3 = distance_3()

        else:
            if sensor_val() == 0:
                straight(DRIVE_SPEED, DRIVE_TIME)

        sleep(0.1)


if __name__ == "__main__":
    main()
