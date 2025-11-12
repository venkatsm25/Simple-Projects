// Project: Smart Traffic Manager - Visual Density Monitor
// Part A: Arduino Controller

// Define the pins for the LEDs
const int greenLED = 11; // Low density
const int yellowLED = 10; // Medium density
const int redLED = 9;   // High density

void setup() {
  // Start serial communication to listen for commands from the computer.
  // 9600 is the baud rate (data speed) - it must match the Python script.
  Serial.begin(9600);

  // Set the LED pins as outputs
  pinMode(greenLED, OUTPUT);
  pinMode(yellowLED, OUTPUT);
  pinMode(redLED, OUTPUT);
}

void loop() {
  // Check if there is any data available to read from the serial port
  if (Serial.available() > 0) {
    // Read the incoming character from the Python script
    char command = Serial.read();

    // --- DIGITAL LOGIC IMPLEMENTATION ---
    // This section acts like a set of logic gates. It checks for a specific input
    // and produces a specific output. Think of it as:
    // IF command IS 'L', THEN green_output IS HIGH.
    // IF command IS 'M', THEN yellow_output IS HIGH.
    // IF command IS 'H', THEN red_output IS HIGH.

    if (command == 'L') { // Low Density
      digitalWrite(greenLED, HIGH);
      digitalWrite(yellowLED, LOW);
      digitalWrite(redLED, LOW);
    }
    else if (command == 'M') { // Medium Density
      digitalWrite(greenLED, LOW);
      digitalWrite(yellowLED, HIGH);
      digitalWrite(redLED, LOW);
    }
    else if (command == 'H') { // High Density
      digitalWrite(greenLED, LOW);
      digitalWrite(yellowLED, LOW);
      digitalWrite(redLED, HIGH);
    }
  }
}