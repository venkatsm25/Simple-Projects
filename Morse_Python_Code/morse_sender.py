import serial
import time

# --- CONFIGURATION ---
# !!! IMPORTANT: Change this to your Arduino Nano's COM port !!!
ARDUINO_PORT = 'COM3' 
BAUD_RATE = 9600
# --- END CONFIGURATION ---

# This is the Morse code "dictionary" from the Arduino,
# but on the Python side. We use it to calculate the
# time we need to wait before sending the next character.
MORSE_CODE_TIMINGS = {
    'A': 2, 'B': 4, 'C': 4, 'D': 3, 'E': 1, 'F': 4, 'G': 3, 'H': 4,
    'I': 2, 'J': 4, 'K': 3, 'L': 4, 'M': 2, 'N': 2, 'O': 3, 'P': 4,
    'Q': 4, 'R': 3, 'S': 3, 'T': 1, 'U': 3, 'V': 4, 'W': 3, 'X': 4,
    'Y': 4, 'Z': 4, '1': 5, '2': 5, '3': 5, '4': 5, '5': 5, '6': 5,
    '7': 5, '8': 5, '9': 5, '0': 5, ' ': 1,
}
# This dictionary stores the *number of parts* (dots/dashes) for each letter.
# We'll use this to estimate how long the Arduino will be busy.

# --- Morse Timings (from Arduino code) ---
BASE_UNIT_MS = 250 # Must match the "baseUnit" in your Arduino code
DOT_TIME = BASE_UNIT_MS
DASH_TIME = BASE_UNIT_MS * 3
PART_SPACE = BASE_UNIT_MS
LETTER_SPACE = BASE_UNIT_MS * 3
WORD_SPACE = BASE_UNIT_MS * 7

def estimate_char_time_ms(char):
    """
    Estimates how long the Arduino will be busy blinking a single character.
    This is the key to making the Python script wait for the Arduino to finish.
    """
    if char not in MORSE_CODE_TIMINGS:
        return 0 # Unknown character, no delay

    if char == ' ':
        return WORD_SPACE

    # This is a good approximation:
    # We don't know the exact mix of dots/dashes, so we'll average
    # (dot+dash)/2 is roughly 2*baseUnit.
    # A more precise way would be to store the full ".-" string, but this is fine.
    
    # Let's use a simpler, more robust estimate:
    # A character is (parts) * (avg_part_time + part_space) + letter_space
    num_parts = MORSE_CODE_TIMINGS.get(char, 0)
    
    # A decent average time for a part (dot or dash) is ~2*BASE_UNIT
    avg_part_duration = (DOT_TIME + DASH_TIME) / 2
    
    # Total time = (parts * (avg_part + part_space)) + time_for_next_letter
    # We will just wait for the letter to finish, then the Arduino code
    # will add its own letterSpace delay.
    
    # Let's try a different, more direct approach.
    # The Arduino code sends one char, blinks it, then waits for the next.
    # The Python script just needs to send the *next* char after the
    # previous one is *probably* finished.
    
    # Let's simplify. We'll use the Arduino's letterSpace as our delay.
    # We send a char, then wait for the letter to be over.
    # This is a "good enough" timer.
    num_parts = MORSE_CODE_TIMINGS.get(char, 1) # Default to 1 part
    
    # An average part is (dot + 3*dot)/2 = 2*dot.
    # Plus a partSpace (1*dot). Total = 3*dot per part.
    # So, time = num_parts * 3 * baseUnit + letterSpace
    
    # Wait, the Arduino code is: blink_part() + delay(partSpace)
    # ...and at the end, Python adds delay(letterSpace)
    
    # Let's do this the easy way.
    # Python sends 'H'. Arduino blinks '....' and is busy.
    # Python sends 'E'. Arduino's serial buffer holds 'E'.
    # After Arduino finishes 'H', it delays(letterSpace), then
    # in the next loop, it reads 'E' and blinks '.'.
    # This is actually fine! We just need a small delay.
    
    # The problem is if we send "HELLO" all at once, the Arduino's
    # 64-byte serial buffer will overflow.
    # We must send... wait... send... wait.
    
    # Let's go back to the Arduino code.
    # void loop() {
    #   if (Serial.available() > 0) {
    #     blinkMorse(Serial.read()); // This function BLOCKS
    #     delay(letterSpace);
    #   }
    # }
    # This means the Arduino CANNOT receive a new char until it
    # finishes blinking the current one + waiting for letterSpace.
    # This makes our Python code's job simple! We just need to
    # add a small "padding" delay.
    
    # Let's re-simplify the Python script.
    pass # No complex timing needed!

def connect_to_arduino(port, baud):
    """Tries to connect to the Arduino on the specified port."""
    print(f"Attempting to connect to Arduino on {port} at {baud} baud...")
    try:
        ser = serial.Serial(port, baud, timeout=2)
        time.sleep(2) # Wait for the connection to establish (Arduino resets)
        print("Connection successful.")
        # Read any startup messages from the Arduino
        print(f"Arduino says: {ser.readline().decode('utf-8').strip()}")
        print(f"Arduino says: {ser.readline().decode('utf-8').strip()}")
        return ser
    except serial.SerialException as e:
        print(f"\n--- ERROR ---")
        print(f"Failed to connect to {port}: {e}")
        print("Please check the following:")
        print("1. Is the Arduino plugged in?")
        print("2. Is the COM port ('{port}') correct? Check the Arduino IDE.")
        print("3. Is the Serial Monitor in the Arduino IDE *closed*?")
        print("---------------")
        return None

def main():
    """Main function to run the text-to-morse sender."""
    
    arduino = connect_to_arduino(ARDUINO_PORT, BAUD_RATE)
    
    if not arduino:
        input("Press Enter to exit.")
        return

    print("\n--- Morse Code Sender ---")
    print("Type your message and press Enter.")
    print("Type 'exit' to quit.")
    print("---------------------------")

    try:
        while True:
            message = input("Enter message: ")
            
            if message.lower() == 'exit':
                print("Exiting...")
                break

            # Convert the message to uppercase and send it
            # one character at a time.
            message = message.upper()
            
            for char in message:
                print(f"Sending: '{char}'")
                
                # Send the single character as bytes
                arduino.write(char.encode('utf-8'))
                
                # IMPORTANT: This is the flow control.
                # We wait for the Arduino to send us back its "debug" line
                # (e.g., "Received: H - Blinking: ....")
                # This tells us it has *finished* the character.
                # We set a timeout just in case.
                
                # Let's modify the Arduino code to be more robust.
                # For now, let's just add a simple delay.
                # The Arduino code from Step 1 has a `delay(letterSpace)` at the end.
                # Let's just add a *bit* more than that.
                
                # New plan: The Arduino code in Step 1 prints a newline
                # *after* it finishes blinking. We can just wait for that.
                
                response = arduino.readline().decode('utf-8').strip()
                print(f"  -> Arduino: {response}")
                
                # If the character was a space, the Arduino code
                # just delays. We'll add a small buffer.
                if char == ' ':
                    time.sleep(WORD_SPACE / 1000.0)
                
                # A small extra pause just in case.
                time.sleep(0.05) 

    except KeyboardInterrupt:
        print("\nCaught Ctrl+C. Exiting...")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if arduino:
            arduino.close()
            print("Serial connection closed.")

if __name__ == "__main__":
    main()