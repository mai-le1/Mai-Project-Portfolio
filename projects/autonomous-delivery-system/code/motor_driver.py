"""
L298N dual DC motor driver control for Raspberry Pi Pico (MicroPython).
"""

from machine import Pin, PWM
from time import sleep

from config import (
    MOTOR_A_CORRECTION,
    MOTOR_A_EN,
    MOTOR_A_IN1,
    MOTOR_A_IN2,
    MOTOR_B_CORRECTION,
    MOTOR_B_EN,
    MOTOR_B_IN3,
    MOTOR_B_IN4,
    PWM_FREQ,
)

motor_a_in1 = Pin(MOTOR_A_IN1, Pin.OUT)
motor_a_in2 = Pin(MOTOR_A_IN2, Pin.OUT)
motor_a_en = PWM(Pin(MOTOR_A_EN))
motor_a_en.freq(PWM_FREQ)

motor_b_in3 = Pin(MOTOR_B_IN3, Pin.OUT)
motor_b_in4 = Pin(MOTOR_B_IN4, Pin.OUT)
motor_b_en = PWM(Pin(MOTOR_B_EN))
motor_b_en.freq(PWM_FREQ)


def _set_pwm(pwm, speed_percent):
    """Set PWM duty from 0–100 percent."""
    duty = int(max(0, min(100, speed_percent)) * 65535 / 100)
    pwm.duty_u16(duty)


def motor_a(direction="stop", speed=0):
    adjusted_speed = speed * MOTOR_A_CORRECTION

    if direction == "forward":
        motor_a_in1.value(0)
        motor_a_in2.value(1)
    elif direction == "backward":
        motor_a_in1.value(1)
        motor_a_in2.value(0)
    else:
        motor_a_in1.value(0)
        motor_a_in2.value(0)
        adjusted_speed = 0

    _set_pwm(motor_a_en, adjusted_speed)


def motor_b(direction="stop", speed=0):
    adjusted_speed = speed * MOTOR_B_CORRECTION

    if direction == "forward":
        motor_b_in3.value(1)
        motor_b_in4.value(0)
    elif direction == "backward":
        motor_b_in3.value(0)
        motor_b_in4.value(1)
    else:
        motor_b_in3.value(0)
        motor_b_in4.value(0)
        adjusted_speed = 0

    _set_pwm(motor_b_en, adjusted_speed)


def stop():
    motor_a()
    motor_b()


def right_turn(speed, duration):
    motor_b("forward", speed)
    motor_a("backward", speed)
    sleep(duration)
    stop()
    sleep(0.1)


def left_turn(speed, duration):
    motor_a("forward", speed)
    motor_b("backward", speed)
    sleep(duration)
    stop()
    sleep(0.1)


def drive(speed, duration):
    motor_a("forward", speed)
    motor_b("forward", speed)
    sleep(duration)
    stop()
    sleep(0.1)


def reverse(speed, duration):
    motor_a("backward", speed)
    motor_b("backward", speed)
    sleep(duration)
    stop()
    sleep(0.1)
