import cv2
import serial
import time
from collections import deque

# --- CONFIGURATION ---
# CORRECTED: Updated to your COM5 port.
ARDUINO_PORT = 'COM5' 
BAUD_RATE = 9600

# --- NEW, MORE SENSITIVE THRESHOLDS FOR CROWD/OBJECT DETECTION ---
# We have significantly lowered these values to make Yellow and Red easier to trigger.
# This means: 0-1 objects = LOW, 2-4 objects = MEDIUM, 5+ objects = HIGH
LOW_THRESHOLD = 2    # Anything less than this (i.e., 0 or 1) is LOW
MEDIUM_THRESHOLD = 5   # Anything less than this (but >= LOW_THRESHOLD) is MEDIUM

# --- NOISE AND SENSITIVITY CONFIGURATION ---
# You can try lowering this value slightly if it's not detecting smaller fingers/objects
MIN_CONTOUR_AREA = 750  
STABILITY_BUFFER_SIZE = 5 # Require 5 consecutive similar readings before changing state

# --- SETUP SERIAL CONNECTION ---
try:
    arduino = serial.Serial(port=ARDUINO_PORT, baudrate=BAUD_RATE, timeout=.1)
    print("Arduino connected successfully on COM5.")
except Exception as e:
    print(f"Error connecting to Arduino on {ARDUINO_PORT}: {e}")
    print("Please check that the Arduino is plugged in and the port is correct.")
    exit()

# --- SETUP VIDEO CAPTURE ---
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open video stream.")
    exit()

backSub = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=50, detectShadows=False)

# --- STABILITY SETUP ---
command_buffer = deque(maxlen=STABILITY_BUFFER_SIZE)
last_sent_command = None

print("Starting crowd density detection... Press 'q' to quit.")
print(f"Logic: 0-{LOW_THRESHOLD-1} objects = GREEN | {LOW_THRESHOLD}-{MEDIUM_THRESHOLD-1} = YELLOW | {MEDIUM_THRESHOLD}+ = RED")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 1. Pre-processing
    fgMask = backSub.apply(frame)

    # 2. Noise Reduction
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    eroded_mask = cv2.erode(fgMask, kernel, iterations=1)
    dilated_mask = cv2.dilate(eroded_mask, kernel, iterations=1)
    _, thresh = cv2.threshold(dilated_mask, 127, 255, cv2.THRESH_BINARY)

    # 3. Find Contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    object_count = 0
    for cnt in contours:
        if cv2.contourArea(cnt) > MIN_CONTOUR_AREA:
            object_count += 1
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
    # 4. Determine density level
    command = ''
    if object_count < LOW_THRESHOLD:
        command = 'L'
    elif object_count < MEDIUM_THRESHOLD:
        command = 'M'
    else:
        command = 'H'
        
    # 5. Stabilization Logic
    command_buffer.append(command)
    if len(command_buffer) == STABILITY_BUFFER_SIZE and len(set(command_buffer)) == 1:
        stable_command = command_buffer[0]
        if stable_command != last_sent_command:
            arduino.write(stable_command.encode())
            print(f"State changed to: {stable_command} (Object Count: {object_count})")
            last_sent_command = stable_command

    # 6. Display visual feedback
    density_level_text = f"Objects: {object_count} -> Current CMD: {command}"
    if last_sent_command:
        density_level_text += f" | Stable State: {last_sent_command}"

    cv2.putText(frame, density_level_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    cv2.imshow('Live Feed', frame)
    cv2.imshow('Cleaned Mask', thresh)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# --- CLEANUP ---
arduino.write(b'L')
arduino.close()
cap.release()
cv2.destroyAllWindows()
print("Program terminated.")