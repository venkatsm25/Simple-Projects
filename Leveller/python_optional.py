# PYTHON SCRIPT (to run on your computer)
# This script reads the angle data sent by the Arduino over the USB cable.
#optional , main function is uploaded to microcontroller from arduino_leveller.cpp

import serial
import time

# Find the correct port for your Arduino in the Arduino IDE (e.g., "COM3" or "/dev/ttyUSB0")
SERIAL_PORT = 'COM3' 
BAUD_RATE = 115200

try:
    arduino = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    print(f"Connected to Arduino on {SERIAL_PORT}...")
    time.sleep(2) # Wait for the connection to establish

    while True:
        if arduino.in_waiting > 0:
            # Read the line from Arduino
            line = arduino.readline().decode('utf-8').strip()
            
            # Check if the line contains what we expect
            if line.startswith("Angle: "):
                try:
                    # Extract the number
                    angle_str = line.replace("Angle: ", "")
                    angle = float(angle_str)
                    
                    # Print a simple text-based level
                    if angle < -2:
                        print(f"<< Tilted Left  ({angle:.2f} degrees)")
                    elif angle > 2:
                        print(f"   Tilted Right >> ({angle:.2f} degrees)")
                    else:
                        print(f"-- LEVEL --     ({angle:.2f} degrees)")
                
                except ValueError:
                    print(f"Could not parse line: {line}")

except serial.SerialException as e:
    print(f"Error: {e}")
except KeyboardInterrupt:
    print("Exiting...")
finally:
    if 'arduino' in locals() and arduino.is_open:
        arduino.close()
        print("Serial connection closed.")