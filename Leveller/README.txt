Smart Digital Leveller System
A high-precision, real-time digital levelling tool built with an Arduino Nano and an MPU-6050 accelerometer. This system provides instant visual feedback via an LED bar graph and can stream high-resolution angle data for logging or integration with other systems.

This project serves as the foundation for a Smart Levelling System designed to calibrate and enhance the efficiency of existing systems, enabling high-precision alignment and establishing a robust, self-correcting mechanism.

📜 Overview
This project replaces a traditional bubble level with a precise digital counterpart. It reads acceleration data from an MPU-6050 gyro/accelerometer module, calculates the precise tilt angle, and displays the "level" on a 5-LED bar graph. The center LED lights up when the surface is perfectly level, while the side LEDs indicate the direction and magnitude of the tilt.

This system is the core sensing component for a larger automated or "smart" system. The angle data can be used to:

Calibrate machinery.

Provide data for a self-correcting platform (e.g., controlling motors).

Log alignment data over time.

✨ Features
High-Precision Sensing: Uses the MPU-6050 for accurate pitch and roll detection.

Instant Visual Feedback: A 5-LED bar graph acts as a visual "bubble," making it intuitive to use.

Real-time Data Output: Streams precise angle data over the serial port, which can be read by a PC (Python, etc.) or another microcontroller.

Scalable: The code can be easily adapted to be more or less sensitive (tiltThreshold) or to control more complex outputs.

🛠️ Hardware Requirements
Microcontroller: 1x Arduino Nano

Sensor: 1x MPU-6050 Gyroscope/Accelerometer Module

Outputs: 5x LEDs (e.g., 2 red, 1 green, 2 red)

Resistors: 5x 220Ω Resistors (one for each LED)

Prototyping: Breadboard and Jumper Wires

Power: USB cable for Arduino Nano

💻 Software & Libraries
This project is programmed using the Arduino IDE (C++).

You must install the following libraries through the Arduino Library Manager:

Adafruit_MPU6050

Adafruit_Sensor

Wire (typically included with the Arduino IDE)

🔌 Circuit & Connections
MPU-6050 Sensor (I2C)
VCC -> Arduino 5V

GND -> Arduino GND

SCL -> Arduino A5

SDA -> Arduino A4

LED Bar Graph
Center LED (Level): Anode (+) to Arduino D4

Left LED: Anode (+) to Arduino D3

Far-Left LED: Anode (+) to Arduino D2

Right LED: Anode (+) to Arduino D5

Far-Right LED: Anode (+) to Arduino D6

All LED Cathodes (-): Connect each to one end of a 220Ω resistor. Connect the other end of all resistors to Arduino GND.

🚀 How to Use
Assemble the Circuit: Build the circuit as described above.

Install Libraries: Open the Arduino IDE, go to Sketch > Include Library > Manage Libraries..., and install the required Adafruit libraries.

Upload Code: Open the .ino file from this repository and upload it to your Arduino Nano.

Test:

Place the breadboard on a surface. The center LED (on D4) should light up when the MPU-6050 sensor is perfectly flat.

Tilt the entire assembly left and right. The LEDs should light up from the center outwards, indicating the direction and magnitude of the tilt.

(Optional) Read Data: Open the Serial Monitor (set to 115200 baud) to see the raw angle data being streamed from the device. You can also use the provided read_level.py Python script to read this data on your PC.

🐍 Python Data Monitoring (Optional)
A Python script, read_level.py, is included to demonstrate how a computer can read and use the angle data.

Requirements:

Bash

pip install pyserial
Usage:

Find your Arduino's serial port (e.g., COM3 on Windows or /dev/ttyUSB0 on Linux).

Update the SERIAL_PORT variable in the script.

Run the script:

Bash

python read_level.py
The console will display a real-time text-based level, showing the precise angle.

📈 Future Enhancements
This project is the first stage. To achieve the goal of a "self-correcting mechanism" that enhances efficiency:

Add Actuators: Integrate servo motors or stepper motors.

Implement PID Control: Use the angle data from this sensor as the input for a PID (Proportional-Integral-Derivative) control loop.

Create Feedback Loop: The PID controller's output would drive the motors to counteract the tilt, automatically returning the system to a perfect level. This creates the "robust, self-correcting mechanism" described in the project goal.

Enhanced using Google Gemini 2.5 Pro