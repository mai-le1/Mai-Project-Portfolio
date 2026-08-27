"""
Shared pin assignments and tuning constants for the autonomous delivery vehicle.
Adjust motor_correction values so both drive wheels match speed.
"""

# --- L298N motor driver (Raspberry Pi Pico) ---
MOTOR_A_IN1 = 6
MOTOR_A_IN2 = 7
MOTOR_A_EN = 8

MOTOR_B_IN3 = 4
MOTOR_B_IN4 = 3
MOTOR_B_EN = 2

MOTOR_A_CORRECTION = 1.0
MOTOR_B_CORRECTION = 1.0
PWM_FREQ = 1000

# --- HC-SR04 ultrasonic sensors (trigger, echo) ---
ULTRASONIC_FRONT = (21, 20)
ULTRASONIC_RIGHT = (19, 18)
ULTRASONIC_LEFT = (17, 16)

# --- Line follower, reed switch, button ---
LINE_SENSOR_PIN = 0
REED_SWITCH_PIN = 15
BUTTON_PIN = 10

# --- Stepper motor (28BYJ-48 via ULN2003) ---
STEPPER_IN1 = 10
STEPPER_IN2 = 11
STEPPER_IN3 = 12
STEPPER_IN4 = 13

# --- Movement tuning ---
DRIVE_SPEED = 35
TURN_SPEED = 35
TURN_TIME = 0.6
DRIVE_TIME = 1.5
OBSTACLE_DISTANCE_CM = 15
PAYLOAD_DISTANCE_CM = 10

# --- Stepper heights (steps) — tune on hardware ---
HEIGHT_PICKUP = 3300
HEIGHT_LIFT = 1350
HEIGHT_DRIVE = 0

# --- IR sensor (ADC) ---
IR_ADC_PIN = 28
IR_THRESHOLD = 1150  # Tune based on bench readings; original notes mention ~2000
