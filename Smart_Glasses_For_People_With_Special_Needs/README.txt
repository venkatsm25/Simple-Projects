# Project MookMitra

**MookMitra** (meaning "Friend of the Mute") is an innovative, cost-effective ecosystem designed to bridge the communication gap for the Deaf and Hard of Hearing (DHH) community in India.

This project provides a seamless, real-time, bidirectional translation system, featuring:

1.  **Smart Glasses** for **Sign-to-Speech** translation.
2.  A **Companion Mobile App** for **Speech-to-Sign** translation.

By leveraging cutting-edge, on-device machine learning, sensor fusion, and a user-centric design, MookMitra aims to deliver an affordable, durable, and offline-capable solution that empowers the DHH community and fosters greater social inclusion.

-----

## 🎯 The Challenge

India is home to one of the world's largest Deaf and Hard of Hearing (DHH) populations, which primarily uses Indian Sign Language (ISL). A pervasive communication barrier exists due to the extremely low ISL fluency among the general hearing population. This disconnect has severe consequences:

  * **🎓 Education:** DHH students struggle in mainstream institutions lacking interpreters, impacting academic performance and development.
  * **🩺 Healthcare:** Communication breakdowns can lead to misdiagnoses, improper treatment, and a lack of informed consent.
  * **💼 Employment:** The communication barrier is a major impediment to employment, limiting career growth and economic independence.
  * **🏙️ Public Services & Daily Life:** Simple tasks like banking, shopping, or using public transport become formidable challenges, leading to dependence and a diminished quality of life.

Current solutions like human interpreters are scarce and costly, while text-based apps are slow and fail to capture the nuance of a real-time conversation.

-----

## 💡 Our Solution: The MookMitra Ecosystem

MookMitra is a holistic, two-part system designed for effortless, natural communication.

### Component 1: The Smart Glasses (Sign-to-Speech)

Worn by the DHH individual, the lightweight smart glasses are the primary translation device.

  * **How it works:** An integrated high-definition camera and an Inertial Measurement Unit (IMU) work together to capture the user's hand gestures, motion, and orientation as they sign.
  * **On-Device Processing:** This dual-sensor data is processed in real-time by a powerful, low-power microcontroller (MCU) embedded in the glasses.
  * **ML Translation:** A sophisticated on-device machine learning model interprets the complex sign language gestures and translates them into text.
  * **Audio Output:** This text is then instantly synthesized into clear, audible speech through a small, outward-facing bone-conduction speaker, allowing a nearby hearing person to understand.

The glasses are engineered for 8-10 hours of daily use, ensuring they are a reliable all-day companion.

### Component 2: The Mobile Application (Speech-to-Sign)

The companion mobile app facilitates the other side of the conversation, allowing a hearing person to communicate back.

  * **How it works:** The hearing person speaks into their smartphone. The MookMitra app uses an advanced Automatic Speech Recognition (ASR) engine to accurately convert their spoken words into text.
  * **Real-Time Animation:** This text is processed and mapped to a comprehensive digital ISL lexicon. The app then generates a fluid, easy-to-understand animation of a 3D avatar performing the signs on the screen.
  * **Offline First:** The app is designed to work offline through downloadable language packs, ensuring functionality even in low-connectivity areas.

-----

## ✨ Key Features

  * **🤝 Bidirectional Communication:** A complete, two-way loop that translates *from* sign language and *to* sign language, enabling a natural conversational flow.
  * **🇮🇳 Multilingual Support:** Recognizing India's linguistic diversity, the system is architected to support multiple languages, starting with **Hindi, Tamil, Telugu, Bengali, and Marathi**.
  * **🔌 Offline Functionality:** The core translation logic for both the glasses and the app is processed on-device. This ensures real-time performance, continuous availability, and no reliance on an internet connection.
  * **🔒 Privacy-Centric:** By performing all computations locally, MookMitra ensures that sensitive conversational data remains completely private. No video or audio streams are ever sent to the cloud.
  * **💸 Affordability & Accessibility:** With a target cost of **₹2,500-₹4,000** per unit, the solution is designed to be economically accessible to a wide audience, breaking the barrier of high-cost assistive technologies.

-----

## 🛠️ Technical Architecture & Methodology

Our technical approach is grounded in state-of-the-art machine learning and efficient hardware design to ensure both high accuracy and practical usability.

### Hardware Architecture (The Smart Glasses)

The smart glasses are a compact integration of several key components:

  * **High-Definition Camera:** A small, wide-angle camera to capture the user's hand and upper-body gestures.
  * **Inertial Measurement Unit (IMU):** A 6 or 9-axis IMU to capture granular data on hand motion, acceleration, and orientation.
  * **Microcontroller Unit (MCU):** A powerful, energy-efficient ARM-based MCU capable of running optimized ML models for on-device inference.
  * **Bone-Conduction Speaker:** Provides audio output without obstructing the user's ears.
  * **High-Density Battery:** A lightweight Li-Po battery optimized for 8-10 hours of continuous use.
  * **Connectivity:** Bluetooth/Wi-Fi modules for pairing with the mobile app and receiving firmware updates.

### The Machine Learning Pipeline

Our innovation lies in the sophisticated, hybrid ML pipeline that powers the translation.

#### 1\. Sign-to-Speech (On-Device ML)

This pipeline is a multi-stage process designed for high accuracy in complex environments:

1.  **Sensor Fusion:** The system captures and synchronizes two data streams: video frames from the **camera** and motion data from the **IMU**.
2.  **Spatial Feature Extraction:** Video frames are fed into a lightweight **Convolutional Neural Network (CNN)**. This model, leveraging foundations from open-source models like MediaPipe Hands, extracts key spatial features—the *shape* of the hand, finger joint positions, and location relative to the body.
3.  **Temporal Context Analysis:** The *sequence* of these spatial features, combined with the IMU's motion data, is fed into a temporal model like a **Long Short-Term Memory (LSTM) or Transformer network**. This model is crucial for understanding context, as the meaning of a sign often depends on the gestures that come before or after it.
4.  **Translation & Synthesis:** The model outputs a final textual translation of the sign sentence. This text is then passed to a lightweight, multilingual **Text-to-Speech (TTS)** engine to generate the final audio output.

> **Key Innovation: IMU Fallback**
> In challenging lighting conditions or when the camera's view is partially blocked, the system can rely more heavily on the rich data from the IMU to maintain translation accuracy, providing a robust fallback mechanism.

#### 2\. Speech-to-Sign (Mobile App Pipeline)

This pipeline is optimized for speed and clarity on a mobile device:

1.  **Speech Recognition (ASR):** The app uses a highly accurate **Indic ASR engine** to convert spoken language into text.
2.  **Natural Language Processing (NLP):** An NLP layer processes the transcribed text to clean it, correct grammatical errors, and understand the core intent.
3.  **Sign Mapping & Animation:** The processed text is translated into a sequence of ISL signs using our digital dictionary. This sequence then drives a realistic **3D avatar** that performs the signs for the DHH user to watch.

### Development Methodology

The project follows an agile, user-centric development lifecycle:

  * **Data Collection:** Collaborating with NGOs and schools for the deaf to build a large, diverse, high-quality video dataset of ISL, covering multiple regional dialects.
  * **Model Training:** Using this dataset to train our custom CNN-LSTM/Transformer models, employing techniques like transfer learning and data augmentation.
  * **Hardware Prototyping:** Iterating on the smart glasses design to optimize ergonomics, power efficiency, and component integration.
  * **Pilot Studies:** Deploying the system in controlled pilot programs to gather user feedback and measure performance using metrics like the System Usability Scale (SUS).

### Risk Mitigation

We have identified and planned for key challenges:

  * **Risk:** High variability in signing styles (regional dialects, individual differences).
      * **Mitigation:** Building robust, region-specific models by collecting a diverse dataset and allowing for user feedback to continuously refine the models.
  * **Risk:** Environmental "noise" (e.g., cluttered backgrounds, poor lighting, loud ambient sounds).
      * **Mitigation:** Our sensor fusion approach is key. The IMU is unaffected by visual noise, and the ASR engine integrates advanced noise-cancellation.
  * **Risk:** User privacy concerns over an "always-on" device.
      * **Mitigation:** Our 100% on-device processing. No video or audio data ever leaves the user's devices, ensuring complete privacy.
  * **Risk:** Latency in real-time translation.
      * **Mitigation:** Rigorous optimization (quantization, pruning) of our ML models to run efficiently on the low-power MCU hardware.

-----

## 🌍 Impact, Scalability, & Future Scope

### Transformative Impact

The societal impact of MookMitra is profound:

  * **Fostering Inclusion:** Empowering DHH individuals to participate fully in education, healthcare, and employment.
  * **Economic Empowerment:** Enhancing employment prospects for the DHH community by breaking communication barriers.
  * **Enhancing Safety & Independence:** Providing the ability to communicate effectively in emergencies or during daily errands.

### Scalability

The MookMitra platform is designed for growth. The software architecture allows for the easy addition of new Indian regional languages and, eventually, other international sign languages. The hardware can be updated with newer, more efficient components as technology evolves.

### Future Roadmap

  * **Augmented Reality (AR) Features:** A future version could display the speech-to-sign 3D avatar as an AR overlay directly within the user's field of view on the glasses, eliminating the need to look at a phone.
  * **Educational Platform:** Expanding the mobile app into a comprehensive platform for the hearing community to learn Indian Sign Language.
  * **IoT Integration:** Allowing DHH users to use sign language to control smart home devices.

In conclusion, MookMitra is more than just a technological device; it is a catalyst for social change, aiming to give a voice to the voiceless and create a more equitable and accessible India.

content enhanced using Google Gemini 2.5Pro


Refernces:
Papatsimouli, M., Kollias, K. F., Lazaridis, L., Maraslidis, G., Michailidis, H., & Sarigiannidis, P. (2022). Real-Time Sign Language Translation Systems: A review study. 2022 11th International Conference on Modern Circuits and Systems Technologies (MOCAST). DOI:10.1109/MOCAST54814.2022.9837666. 
ResearchGate

Damdoo, R. (2025). An integrative survey on Indian Sign Language recognition and interpretation. IET Image Processing. 
IET Research Journals

Joshi, A., et al. (2023). ISLTranslate: Dataset for Translating Indian Sign Language. Findings of ACL. 
ACL Anthology

Vashisth, H.K., Tarafder, T., Aziz, R., Arora, M., & Alpana. (2023). Hand Gesture Recognition in Indian Sign Language Using Deep Learning. Engineering Proceedings, 59(1):96. DOI:10.3390/engproc2023059096. 
MDPI

Patil, R. (2021). Indian Sign Language Recognition using Convolutional Neural Networks. ITM Conferences, ICACC 2021. 
ITM Conferences

Katoch, S., et al. (2022). Indian Sign Language Recognition using SURF with Bag of Visual Words Model. (Alphabet & digits recognition) Elsevier publication. 
ScienceDirect

Shetty, S. (2024). A Real-Time Indian Sign Language Translator with PoseNet Algorithms. ScienceDirect article. 
ScienceDirect

Liang, Z. (2023). Sign Language Translation: A Survey of Approaches and Future Directions. Electronics, 12(12):2678. 
MDPI

IJISAE. (2024). Translation of Indian Sign Language to Text-A Review. (International Journal of …) 
IJISAE

Jain, S. (2015). Indian Sign Language Character Recognition. Report, IIT Kharagpur.
cse.iitk.ac.in
