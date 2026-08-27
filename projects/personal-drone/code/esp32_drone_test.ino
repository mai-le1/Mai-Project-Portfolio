#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>

// =====================
// Pin setup
// =====================
const int MOTOR_1 = 25;
const int MOTOR_2 = 26;
const int MOTOR_3 = 32;
const int MOTOR_4 = 33;

const int SDA_PIN = 21;
const int SCL_PIN = 22;

const int BATTERY_ADC = 35;

// =====================
// PWM setup
// =====================
const int PWM_FREQ = 20000;      // 20 kHz
const int PWM_RESOLUTION = 8;    // 0-255

// =====================
// MPU6050
// =====================
Adafruit_MPU6050 mpu;

// =====================
// Motor/throttle values
// =====================
int throttle = 0;          // Base motor speed: 0-255
int minThrottle = 0;
int maxThrottle = 220;     // Keep below 255 for testing

// =====================
// Stabilization settings
// Start small. Too high = unstable/crazy motors.
// =====================
float Kp_roll = 12.0;
float Kp_pitch = 12.0;

float targetRoll = 0.0;
float targetPitch = 0.0;

// Complementary filter angle estimate
float rollAngle = 0.0;
float pitchAngle = 0.0;

unsigned long lastTime = 0;

// =====================
// Safety
// =====================
bool motorsArmed = false;

void setup() {
  Serial.begin(115200);
  delay(1000);

  Serial.println();
  Serial.println("ESP32 Drone Test - No Bluetooth");

  // I2C setup
  Wire.begin(SDA_PIN, SCL_PIN);

  // MPU6050 setup
  if (!mpu.begin()) {
    Serial.println("ERROR: MPU6050 not found.");
    Serial.println("Check VCC, GND, SDA, SCL.");
    while (1) {
      delay(500);
    }
  }

  Serial.println("MPU6050 detected.");

  // MPU settings
  mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
  mpu.setGyroRange(MPU6050_RANGE_500_DEG);
  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);

  // Attach PWM pins
  ledcAttach(MOTOR_1, PWM_FREQ, PWM_RESOLUTION);
  ledcAttach(MOTOR_2, PWM_FREQ, PWM_RESOLUTION);
  ledcAttach(MOTOR_3, PWM_FREQ, PWM_RESOLUTION);
  ledcAttach(MOTOR_4, PWM_FREQ, PWM_RESOLUTION);

  stopMotors();

  lastTime = micros();

  Serial.println("Commands:");
  Serial.println("a = arm motors");
  Serial.println("d = disarm motors");
  Serial.println("+ = increase throttle");
  Serial.println("- = decrease throttle");
  Serial.println("0 = stop");
  Serial.println("1 = low throttle");
  Serial.println("2 = medium throttle");
  Serial.println("3 = higher throttle");
  Serial.println();
  Serial.println("REMOVE PROPELLERS FOR TESTING.");
}

void loop() {
  readSerialCommands();

  // Read IMU
  sensors_event_t accel, gyro, temp;
  mpu.getEvent(&accel, &gyro, &temp);

  // Calculate elapsed time
  unsigned long now = micros();
  float dt = (now - lastTime) / 1000000.0;
  lastTime = now;

  // Avoid weird dt values
  if (dt <= 0 || dt > 0.1) {
    dt = 0.01;
  }

  updateAngles(accel, gyro, dt);

  // Calculate stabilization correction
  float rollError = targetRoll - rollAngle;
  float pitchError = targetPitch - pitchAngle;

  int rollCorrection = (int)(Kp_roll * rollError);
  int pitchCorrection = (int)(Kp_pitch * pitchError);

  // Limit correction so it does not go crazy
  rollCorrection = constrain(rollCorrection, -40, 40);
  pitchCorrection = constrain(pitchCorrection, -40, 40);

  if (motorsArmed && throttle > 0) {
    mixAndWriteMotors(throttle, rollCorrection, pitchCorrection);
  } else {
    stopMotors();
  }

  printDebug();
  delay(20); // ~50 Hz loop for first test
}

// =====================
// Serial commands
// =====================
void readSerialCommands() {
  if (Serial.available()) {
    char cmd = Serial.read();

    if (cmd == 'a') {
      motorsArmed = true;
      throttle = 0;
      Serial.println("Motors ARMED. Use + slowly.");
    }

    else if (cmd == 'd') {
      motorsArmed = false;
      throttle = 0;
      stopMotors();
      Serial.println("Motors DISARMED.");
    }

    else if (cmd == '+') {
      throttle += 5;
      throttle = constrain(throttle, minThrottle, maxThrottle);
    }

    else if (cmd == '-') {
      throttle -= 5;
      throttle = constrain(throttle, minThrottle, maxThrottle);
    }

    else if (cmd == '0') {
      throttle = 0;
      stopMotors();
    }

    else if (cmd == '1') {
      throttle = 80;
    }

    else if (cmd == '2') {
      throttle = 120;
    }

    else if (cmd == '3') {
      throttle = 160;
    }

    Serial.print("Throttle = ");
    Serial.println(throttle);
  }
}

// =====================
// Angle estimation
// =====================
void updateAngles(sensors_event_t accel, sensors_event_t gyro, float dt) {
  // Accelerometer angle estimate in degrees
  float accelRoll = atan2(accel.acceleration.y, accel.acceleration.z) * 180.0 / PI;
  float accelPitch = atan2(-accel.acceleration.x,
                           sqrt(accel.acceleration.y * accel.acceleration.y +
                                accel.acceleration.z * accel.acceleration.z)) * 180.0 / PI;

  // Gyro values are in rad/s from Adafruit library
  float gyroRollRate = gyro.gyro.x * 180.0 / PI;
  float gyroPitchRate = gyro.gyro.y * 180.0 / PI;

  // Complementary filter
  rollAngle = 0.98 * (rollAngle + gyroRollRate * dt) + 0.02 * accelRoll;
  pitchAngle = 0.98 * (pitchAngle + gyroPitchRate * dt) + 0.02 * accelPitch;
}

// =====================
// Motor mixing
// =====================
// Layout assumption:
//
//        FRONT
//
//     M1       M2
//
//     M3       M4
//
//        BACK
//
// If correction acts backwards, swap signs later.
// =====================
void mixAndWriteMotors(int baseThrottle, int rollCorrection, int pitchCorrection) {
  int m1 = baseThrottle - pitchCorrection + rollCorrection;
  int m2 = baseThrottle - pitchCorrection - rollCorrection;
  int m3 = baseThrottle + pitchCorrection + rollCorrection;
  int m4 = baseThrottle + pitchCorrection - rollCorrection;

  m1 = constrain(m1, 0, 255);
  m2 = constrain(m2, 0, 255);
  m3 = constrain(m3, 0, 255);
  m4 = constrain(m4, 0, 255);

  ledcWrite(MOTOR_1, m1);
  ledcWrite(MOTOR_2, m2);
  ledcWrite(MOTOR_3, m3);
  ledcWrite(MOTOR_4, m4);
}

void stopMotors() {
  ledcWrite(MOTOR_1, 0);
  ledcWrite(MOTOR_2, 0);
  ledcWrite(MOTOR_3, 0);
  ledcWrite(MOTOR_4, 0);
}

// =====================
// Battery voltage
// =====================
float readBatteryVoltage() {
  int raw = analogRead(BATTERY_ADC);

  // ESP32 ADC approx conversion.
  // This is not perfectly accurate without calibration.
  float adcVoltage = (raw / 4095.0) * 3.3;

  // Your divider is 100k + 100k, so multiply by 2.
  float batteryVoltage = adcVoltage * 2.0;

  return batteryVoltage;
}

// =====================
// Debug printing
// =====================
void printDebug() {
  static unsigned long lastPrint = 0;

  if (millis() - lastPrint >= 500) {
    lastPrint = millis();

    Serial.print("Armed: ");
    Serial.print(motorsArmed ? "YES" : "NO");

    Serial.print(" | Throttle: ");
    Serial.print(throttle);

    Serial.print(" | Roll: ");
    Serial.print(rollAngle);

    Serial.print(" | Pitch: ");
    Serial.print(pitchAngle);

    Serial.print(" | Battery: ");
    Serial.print(readBatteryVoltage());
    Serial.println(" V");
  }
}
