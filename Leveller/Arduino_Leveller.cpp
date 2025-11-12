/*
 * ARDUINO (C++) CODE FOR DIGITAL LEVELLER
 * -----------------------------------------
 * This code reads tilt data from an MPU-6050 sensor and displays the 'level'
 * on a 5-LED bar graph.
 * * Connections:
 * - MPU-6050 SCL: Arduino Nano A5
 * - MPU-6050 SDA: Arduino Nano A4
 * - MPU-6050 VCC: Arduino 5V
 * - MPU-6050 GND: Arduino GND
 * * - LED 1 (Far Left): Nano D2
 * - LED 2 (Left):     Nano D3
 * - LED 3 (Center):   Nano D4
 * - LED 4 (Right):    Nano D5
 * - LED 5 (Far Right):Nano D6
 * * - All LED anodes (long legs) to their D pin.
 * - All LED cathodes (short legs) through a 220-ohm resistor to GND.
 */

#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>

Adafruit_MPU6050 mpu;

// Define the Arduino pins for the LEDs
const int ledPins[] = {2, 3, 4, 5, 6}; // Far-Left, Left, Center, Right, Far-Right
const int numLeds = 5;
const int centerLedIndex = 2; // Index of the center LED (pin D4)

// Tilt sensitivity. Smaller numbers are more sensitive.
// This defines the angle (in degrees) for each "step"
const float tiltThreshold = 2.0; 

void setup() {
  Serial.begin(115200);

  // Initialize all LED pins as outputs
  for (int i = 0; i < numLeds; i++) {
    pinMode(ledPins[i], OUTPUT);
  }

  // Initialize MPU-6050
  if (!mpu.begin()) {
    Serial.println("Failed to find MPU6050 chip");
    while (1) {
      // Blink center LED as an error code
      digitalWrite(ledPins[centerLedIndex], HIGH);
      delay(100);
      digitalWrite(ledPins[centerLedIndex], LOW);
      delay(100);
    }
  }
  Serial.println("MPU6050 Found!");

  // --- Optional: Calibrate Sensor ---
  // For high precision, you should calibrate the sensor's offsets.
  // Place it on a perfectly flat surface and run a calibration sketch first.
  // For this example, we'll use generic settings.
  // mpu.setAccelOffsets(-1500, -500, 1000); // Example: Set your own offsets here
}

void loop() {
  // Get new sensor event
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);

  // Calculate the tilt angle (Pitch)
  // We use atan2 for a stable angle calculation from the accelerometer data
  // This calculates tilt around the Y-axis (like a plane's nose-up/down)
  // For tilt around X-axis (roll), use (a.acceleration.y, a.acceleration.z)
  float angle = atan2(a.acceleration.x, a.acceleration.z) * RAD_TO_DEG;

  // Print the angle to the Serial Monitor for debugging
  Serial.print("Angle: ");
  Serial.println(angle);

  // Update the LEDs based on the angle
  updateLeds(angle);

  delay(100); // Small delay to prevent flickering
}

void updateLeds(float angle) {
  // Turn all LEDs off first
  for (int i = 0; i < numLeds; i++) {
    digitalWrite(ledPins[i], LOW);
  }

  // Determine which LED to light up
  if (angle < -tiltThreshold * 2) {
    // Tilted far left
    digitalWrite(ledPins[0], HIGH); 
  } else if (angle < -tiltThreshold) {
    // Tilted left
    digitalWrite(ledPins[1], HIGH);
  } else if (angle > tiltThreshold * 2) {
    // Tilted far right
    digitalWrite(ledPins[4], HIGH);
  } else if (angle > tiltThreshold) {
    // Tilted right
    digitalWrite(ledPins[3], HIGH);
  } else {
    // Level
    digitalWrite(ledPins[centerLedIndex], HIGH); 
  }
}