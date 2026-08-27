"""
Line-following sensor input.
"""

from machine import Pin

from config import LINE_SENSOR_PIN

line_sen = Pin(LINE_SENSOR_PIN, Pin.IN)


def sensor_val():
    """Return 1 when the sensor sees the line, 0 otherwise."""
    return line_sen.value()
