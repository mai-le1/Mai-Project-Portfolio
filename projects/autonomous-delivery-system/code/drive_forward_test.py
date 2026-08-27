"""
Drive forward ~4 ft test (Raspberry Pi Pico).

Uses motor speed and duration to approximate distance:
  length = 1.2192 m (4 ft), pace = 0.6 m/s → duration ≈ 2.03 s

Original test used sleep(7) with motors at 40/41 — adjust speed and
duration in config or below to match your chassis.
"""

from time import sleep

import motor_driver

LENGTH_M = 1.2192  # 4 feet
PACE_MPS = 0.6
DURATION_S = LENGTH_M / PACE_MPS

# Slight correction so both wheels track straight
MOTOR_A_SPEED = 40
MOTOR_B_SPEED = 41


def main():
    print("Driving forward for {:.1f} s (~{:.2f} m)".format(DURATION_S, LENGTH_M))

    motor_driver.motor_a("forward", MOTOR_A_SPEED)
    motor_driver.motor_b("forward", MOTOR_B_SPEED)
    sleep(DURATION_S)
    motor_driver.stop()

    print("Done.")


if __name__ == "__main__":
    main()
