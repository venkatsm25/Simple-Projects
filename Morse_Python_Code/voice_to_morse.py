import serial
import time
import sounddevice as sd
import vosk
import queue
import json
import sys

# --- CONFIGURATION ---
# !!! IMPORTANT: Change this to your Arduino Nano's COM port !!!
ARDUINO_PORT = 'COM3' 
BAUD_RATE = 9600
MODEL_PATH = 'model' # The folder you just downloaded and renamed
DEVICE_SAMPLERATE = 16000 # Standard sample rate for Vosk models
# --- END CONFIGURATION ---

q = queue.Queue()

def connect_to_arduino(port, baud):
    """Tries to connect to the Arduino."""
    print(f"Connecting to Arduino on {port}...")
    try:
        ser = serial.Serial(port, baud, timeout=2)
        time.sleep(2) # Wait for connection
        print("Connection successful.")
        ser.reset_input_buffer()
        # Read Arduino's startup messages
        print(f"Arduino says: {ser.readline().decode('utf-8').strip()}")
        print(f"Arduino says: {ser.readline().decode('utf-8').strip()}")
        return ser
    except serial.SerialException as e:
        print(f"\n--- ERROR: Could not connect to Arduino. ---")
        print(f"Details: {e}")
        print("Please check: 1. Is it plugged in? 2. Is the COM port correct? 3. Is the Serial Monitor closed?")
        return None

def send_message_to_arduino(ser, message):
    """Sends a message, char by char, waiting for the Arduino's response."""
    if not ser:
        print("Cannot send: Arduino is not connected.")
        return

    print(f"Sending to Arduino: '{message}'")
    message = message.upper() # Arduino code expects uppercase

    for char in message:
        # Send the character
        ser.write(char.encode('utf-8'))
        
        # Wait for the Arduino to finish blinking and send its debug line
        response = ser.readline().decode('utf-8').strip()
        print(f"  -> Arduino: {response}")
        
        # If the character was a space, the Arduino code
        # just delays. We'll add a small buffer.
        if char == ' ':
            time.sleep(2.0) # Wait for the wordSpace (7 * 250ms = 1.75s)
        
    print("--- Message complete ---")

def mic_callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio chunk."""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

def main():
    print("--- Voice-to-Morse Engine ---")
    
    # 1. Connect to Arduino
    arduino = connect_to_arduino(ARDUINO_PORT, BAUD_RATE)
    if not arduino:
        input("Press Enter to exit.")
        return

    # 2. Load Vosk Model
    print(f"Loading Vosk model from '{MODEL_PATH}'...")
    try:
        model = vosk.Model(MODEL_PATH)
    except Exception as e:
        print(f"\n--- ERROR: Could not load model. ---")
        print(f"Details: {e}")
        print(f"Did you download the Indian English model and rename the folder to 'model'?")
        print("It MUST be in the same directory as this script.")
        arduino.close()
        input("Press Enter to exit.")
        return
        
    print("Model loaded successfully.")
    
    # 3. Start Audio Stream
    try:
        print("\n--- Listening... ---")
        print("Speak into your microphone. Pause to send.")
        print("Say 'exit' or 'quit' to stop.")
        
        # Create a recognizer object
        recognizer = vosk.KaldiRecognizer(model, DEVICE_SAMPLERATE)
        
        # Open the microphone stream
        with sd.RawInputStream(samplerate=DEVICE_SAMPLERATE, 
                               blocksize=8000, 
                               device=None, # Use default mic
                               dtype='int16',
                               channels=1, 
                               callback=mic_callback):

            while True:
                # Get audio data from the queue (filled by mic_callback)
                data = q.get()
                
                if recognizer.AcceptWaveform(data):
                    # User paused. Get the "final" result.
                    result_json = recognizer.FinalResult()
                    result_dict = json.loads(result_json)
                    text = result_dict['text']
                    
                    if text:
                        print(f"\nRecognized: '{text}'")
                        
                        # Check for exit command
                        if text.lower() == 'exit' or text.lower() == 'quit':
                            print("Exit command received. Shutting down.")
                            break
                        
                        # Send the recognized text to the Arduino
                        send_message_to_arduino(arduino, text)
                        print("\nListening...")
                else:
                    # Show partial results as the user is speaking
                    result_json = recognizer.PartialResult()
                    result_dict = json.loads(result_json)
                    partial_text = result_dict['partial']
                    
                    # Print on one line, overwriting itself
                    print(f"Speaking: {partial_text.ljust(50)}", end='\r')

    except KeyboardInterrupt:
        print("\nCaught Ctrl+C. Shutting down...")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if arduino:
            arduino.close()
            print("Serial connection closed.")

if __name__ == "__main__":
    main()