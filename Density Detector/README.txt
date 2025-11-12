Smart Crowd Density Monitor & Traffic Control System

This project is a real-time smart monitoring system that uses computer vision (OpenCV) to detect crowd or traffic density and triggers corresponding hardware signals via an Arduino. It serves as a powerful prototype for smart traffic lights, crowd control systems, or automated resource management.

The system's logic is split into two parts:

Computer Vision (Python): A Python script running on a PC uses a webcam to "see" the area. It counts the number of objects (people, cars, etc.) and classifies the density as Low, Medium, or High.

Hardware Controller (Arduino): The Arduino receives a simple command (L, M, or H) from the Python script and lights up a corresponding LED (Green, Yellow, or Red) to provide immediate visual feedback.

📜 Features

Real-Time Video Processing: Uses OpenCV for live video capture and analysis.

Object/Crowd Detection: Implements background subtraction to effectively isolate and count moving objects.

Configurable Sensitivity: Easily adjust object detection thresholds, minimum object size, and density levels in the Python script.

State Stabilization: Includes a stability buffer to prevent rapid, flickering state changes, ensuring a more robust output (e.g., won't flicker from Green to Yellow and back rapidly).

Serial Communication: A simple and reliable serial protocol (L, M, H) links the PC-based vision script to the Arduino hardware.

Visual Hardware Feedback: A 3-LED system (Green, Yellow, Red) provides a clear, real-world indication of the currently detected density level.

🛠️ System Architecture

Capture: The density_detector.py script captures video from a webcam (cv2.VideoCapture).

Process: Each frame is processed using OpenCV's BackgroundSubtractorMOG2. This isolates moving objects from the static background.

Analyze: The script applies noise reduction (erosion and dilation) and then finds contours (outlines of detected objects). It filters these contours by area (MIN_CONTOUR_AREA) to count only significant objects.

Classify: The object_count is compared against LOW_THRESHOLD and MEDIUM_THRESHOLD to classify the density as:

'L' (Low): Green LED

'M' (Medium): Yellow LED

'H' (High): Red LED

Stabilize & Transmit: To avoid flickering, the system waits for STABILITY_BUFFER_SIZE (e.g., 5) consecutive identical readings before sending the new command to the Arduino via the serial port.

Execute: The sketch_oct9b.ino running on the Arduino listens for a character. When it receives 'L', 'M', or 'H', it updates the LEDs, turning on the correct one and turning the other two off.

Hardware & Software Requirements

Hardware

PC/Laptop: To run the Python script.

Webcam: For video input.

Arduino: Any model (Uno, Nano, etc.)

LEDs: 1x Green, 1x Yellow, 1x Red

Resistors: 3x 220Ω (or similar, one for each LED)

Breadboard & Jumper Wires

Software

Python 3:

OpenCV: pip install opencv-python

PySerial: pip install pyserial

Arduino IDE: To upload the .ino sketch.

🔌 Setup & Installation

1. Hardware Connections (Arduino)

Connect the anode (long leg) of the Green LED to Digital Pin 11 on the Arduino.

Connect the anode (long leg) of the Yellow LED to Digital Pin 10 on the Arduino.

Connect the anode (long leg) of the Red LED to Digital Pin 9 on the Arduino.

Connect the cathode (short leg) of each LED to one end of a 220Ω resistor.

Connect the other end of all three resistors to the Arduino's GND pin.

2. Arduino Setup

Open sketch_oct9b.ino in the Arduino IDE.

Connect your Arduino to your PC.

Select the correct Board and Port from the Tools menu.

Click Upload to flash the sketch to the Arduino.

3. Python Setup

Install the required Python libraries:

pip install opencv-python pyserial


IMPORTANT: Identify your Arduino's serial port.

Windows: Open Device Manager. Look under "Ports (COM & LPT)" for your Arduino (e.g., COM5).

Mac/Linux: Open a terminal and run ls /dev/tty.*. Look for something like /dev/tty.usbmodem... or /dev/ttyUSB0.

Open the density_detector.py script and update the ARDUINO_PORT variable on line 8 to match your port:

# Example for Windows
ARDUINO_PORT = 'COM5' 

# Example for Mac/Linux
# ARDUINO_PORT = '/dev/tty.usbmodem14201'


🚀 Running the Project

Ensure your Arduino is connected and the hardware is wired correctly.

Plug in your webcam.

Run the Python script from your terminal:

python density_detector.py


Two windows will appear:

'Live Feed': Your webcam video with detected objects outlined in green.

'Cleaned Mask': The black & white "vision" of the background subtractor.

The terminal will print status messages (e.g., "Arduino connected successfully...").

Move objects (like your hand) in front of the camera. As the object count changes, the terminal will print the new state, and the LEDs on your Arduino will change from Green to Yellow to Red.

Press 'q' in the OpenCV window to quit the program.

⚙️ Configuration &Tuning

You can easily fine-tune the system's performance by editing the configuration variables at the top of density_detector.py:

ARDUINO_PORT: Must match your Arduino's port.

BAUD_RATE: Must match the Serial.begin(9600) rate in the Arduino sketch.

LOW_THRESHOLD: The number of objects required to switch from Low (Green) to Medium (Yellow).

MEDIUM_THRESHOLD: The number of objects required to switch from Medium (Yellow) to High (Red).

MIN_CONTOUR_AREA: The minimum size (in pixels) for an object to be counted. Increase this to ignore smaller objects/noise. Decrease this to detect smaller objects.

STABILITY_BUFFER_SIZE: The number of consecutive frames the system must see the same state before sending a command. Increase this for more stability (slower response). Decrease this for a faster, more "twitchy" response.


This documentation and program was structured and enhanced using Google Gemini 2.5 Pro.



Refernces:

B. N. Nandhini and R. Manoharan, “Smart Traffic Control System Using Image Processing,” International Journal of Computer Science Trends and Technology (IJCST), Vol. 4, Issue 2, Mar-Apr 2016.
— Explains how background subtraction and contour-based methods can detect traffic density using OpenCV.

A. Kumar, M. Singh, “Automatic Traffic Density Estimation and Signal Timing Using Image Processing,” International Journal of Advanced Research in Computer Engineering & Technology, Vol. 4, Issue 3, Mar 2015.
— Demonstrates real-time control of signal timing using density classification similar to your L-M-H logic.

N. P. Kothari et al., “Smart Traffic Control System Using IoT,” IEEE Conference on Recent Advances in Electronics and Communication Technology (ICRAECT), 2017.
— Explores combining Arduino/ESP modules with cloud connectivity for traffic monitoring.

Learning OpenCV 4: Computer Vision with Python and OpenCV Library
By Adrian Kaehler & Gary Bradski (O’Reilly, 2020)
— The definitive guide to OpenCV and background subtraction techniques.

Exploring Arduino: Tools and Techniques for Engineering Wizardry
By Jeremy Blum (Wiley, 2nd Ed., 2021)
— Great explanation of serial communication and interfacing sensors/LEDs with microcontrollers.

Digital Image Processing
By Rafael C. Gonzalez & Richard E. Woods (Pearson, 4th Ed., 2018)
— Core concepts behind motion detection, thresholding, and noise reduction.

Embedded Systems: Real-Time Interfacing to the MSP432 Microcontroller
By Jonathan W. Valvano (2017)
— Applies well to timing, stability buffers, and serial protocol design.
