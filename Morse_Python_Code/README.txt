# Hybrid Digital Logic System: Speech and Text to Morse Code Converter

![Photo of the project circuit with Arduino Nano and LED output](img/morse-code.png)

This project is a hybrid digital logic system that translates both text and real-time speech into International Morse Code, with the output displayed visually using high-intensity LEDs. The system integrates Python for high-level software logic and an Arduino Nano for low-level hardware control.

## 🌟 Core Features

* **Text-to-Morse:** Converts any user-inputted text string into its corresponding Morse code.
* **Speech-to-Morse:** Utilizes the **Vosk API** for real-time speech-to-text processing, which is then immediately encoded into Morse.
* **Visual Output:** Provides a real-time visual representation of the Morse code signals (dots and dashes) using a high-intensity LED array.
* **Hybrid System:** Demonstrates a practical application of digital logic principles by interfacing a PC-based Python application with an embedded Arduino microcontroller.

## 🛠️ How It Works (Proposed Methodology)

The system operates in a clear, sequential flow:

1.  **Input:** The user provides input through one of two methods:
    * **Text Input:** Typing a string directly into the system.
    * **Speech Input:** Speaking into a microphone.
2.  **Processing:**
    * If the input is speech, the **Vosk API** is used to process the audio and convert it into a text string.
    * The resulting text string (either from direct input or Vosk) is then processed by a Python script.
    * This script encodes the text into the correct sequence of dots and dashes based on International Morse Code rules.
3.  **Transmission:** The Python script sends the encoded signals to the Arduino Nano via serial communication.
4.  **Hardware Output:** The Arduino Nano interprets these signals and controls the GPIO pins connected to the LED array, causing the LEDs to blink in the precise pattern of the Morse code message.

## 💻 Technology Stack

### Software Requirements
* **Python:** For the main application logic, text processing, and API integration.
* **Vosk Speech Recognition API:** For converting real-time speech to text.
* **Arduino IDE:** For programming the Arduino Nano microcontroller.
* **PySerial:** Python library to manage serial communication between the PC and the Arduino.

### Hardware Requirements
* **Arduino Nano:** The microcontroller responsible for interpreting signals and controlling the hardware.
* **High-Intensity LEDs:** Used for the visual output of the Morse code.
* **PC with Microphone:** To run the Python application and capture speech input.
* **Breadboard, Resistors, and Jumper Wires:** For constructing the circuit.

## 📈 Results

The system successfully converts both text and live speech inputs into visual Morse code.
* LEDs blink accurately to represent dots and dashes.
* Real-time speech-to-visual output was achieved through effective API and microcontroller communication.
* Efficient serial communication between the Python application and the Arduino was verified.
* Output validated for various test inputs (e.g., “HELP”, “SOS”, “CODE”).

## 🚀 Future Scope

While the current system is fully functional, it has a strong foundation for future enhancements:

* **Wireless Integration:** Integrating Bluetooth or Wi-Fi modules for remote communication and control.
* **LCD Display:** Adding an LCD screen to display the plain text or Morse code textually alongside the visual LED output.
* **Miniaturization:** Developing the project into a compact, portable communication device.
* **AI Enhancement:** Exploring AI-based emotion recognition from the speech input.
* **Potential Applications:** The device could be adapted for use in rescue missions, defense systems, or as a communication aid for speech-impaired individuals.

---

> **Note:** The programming code and content for this project were enhanced and refined using Google Gemini 2.5 Pro.



References:
Choudhury, R.R. “Morse Code-Enabled Speech Recognition for Individuals with Visual and Hearing Impairments.” arXiv preprint arXiv:2407.14525 (2024). 
arXiv

“Multi-Modal Morse Code Translator: Communicate via Sound, Gesture & Eye-Blink.” Vasudha Manvith. (2024). 
Semantic Scholar

Goswami, M., Hussain, A., Kothakonda, S., Dubey, R., Vargantwar, L., Khanorkar, M., Prasad, A. “Gesture Language Translator using Morse Code.” i-manager’s Journal on Computer Science, Vol 12(3), 59-65 (2024). 
i-manager publications

Pinjarkar, U., Kadam, A., Kasbe, K., Popalghat, S. “Morse Code Translator to Convert Text to Morse Code and Morse to Text.” Journal of Web Engineering & Technology, 11(01), 6-11 (2024). 
STM Journals

Akare, U.P., Bhure, K., Sonkusre, A., Ganorkar, A., Barapatre, M., Roychowdhury, P. “Morse Code Detector Using Machine Learning.” International Journal of Advanced Research in Computer and Communication Engineering, Vol 13 Issue 4, April 2024. 
Peer-reviewed Journal

Nicolaou, N., Georgiou, J. “Towards a Morse Code-Based Non-invasive Thought-to-Speech Converter.” In: Biomedical Engineering Systems and Technologies (BIOSTEC 2008). CCIS vol 25, pp 123-135. Springer, 2008. 
SpringerLink

“Morse Code Converter Using Arduino for Real-Time Applications.” Swanirman Consultancy, March 2025. 
swanirmanconsultancy.in

“Morse Code Translator.” JETIRGX06066, July 2025, Volume 12, Issue 7. Naik Prajwal, Preetham, Vaibhav K.V., Chethan Raj, Aravind Naik. 
Jetir
