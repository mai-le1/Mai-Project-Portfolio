"""
HC-SR04 ultrasonic distance sensors (front, right, left).
Requires the hcsr04.py driver on the Pico filesystem.
"""

from hcsr04 import HCSR04

from config import ULTRASONIC_FRONT, ULTRASONIC_LEFT, ULTRASONIC_RIGHT

sensor_front = HCSR04(
    trigger_pin=ULTRASONIC_FRONT[0],
    echo_pin=ULTRASONIC_FRONT[1],
)
sensor_right = HCSR04(
    trigger_pin=ULTRASONIC_RIGHT[0],
    echo_pin=ULTRASONIC_RIGHT[1],
)
sensor_left = HCSR04(
    trigger_pin=ULTRASONIC_LEFT[0],
    echo_pin=ULTRASONIC_LEFT[1],
)


def read_distances():
    """Return (front, right, left) distances in cm."""
    return (
        sensor_front.distance_cm(),
        sensor_right.distance_cm(),
        sensor_left.distance_cm(),
)


# Aliases matching original sample-code naming
distance1 = lambda: sensor_front.distance_cm()
distance2 = lambda: sensor_right.distance_cm()
distance3 = lambda: sensor_left.distance_cm()
