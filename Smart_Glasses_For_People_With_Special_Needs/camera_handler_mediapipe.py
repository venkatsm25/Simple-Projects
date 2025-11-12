# Mook Mitra - Camera Handler (MediaPipe Version)
# FINAL, DEFINITIVE VERSION: Connects directly to index 0 with enhanced diagnostics.

def start_camera():
    """
    Initializes webcam directly at index 0 and uses MediaPipe for robust hand tracking.
    """
    # --- Just-in-Time Imports ---
    import cv2
    import numpy as np
    import mediapipe as mp
    import time
    from ml_processor import load_model, predict_sign
    from text_to_speech_handler import speak

    hands = None
    cap = None
    
    try:
        # --- Initialize MediaPipe Hands ---
        print("[INFO] Initializing MediaPipe Hands...")
        mp_hands = mp.solutions.hands
        hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)
        mp_drawing = mp.solutions.drawing_utils
        print("[INFO] MediaPipe Hands initialized successfully.")

        # --- Model Loading ---
        print("[INFO] Loading Keras model...")
        model = load_model()
        if model is None:
            print("[ERROR] Failed to load the Sign Language ML model.")
            return "Model loading error."
        print("[INFO] Keras model loaded successfully.")

        # --- Direct Camera Initialization ---
        camera_index = 0
        print(f"[INFO] Attempting to open webcam at index {camera_index}...")
        cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)
        
        if not cap.isOpened():
            print(f"[ERROR] CRITICAL: Could not open webcam at index {camera_index}.")
            return f"Camera connection error at index {camera_index}."
        
        # --- CRITICAL FIX: Give the camera 1 second to initialize ---
        print("[INFO] Webcam opened. Waiting 1 second for driver to initialize...")
        time.sleep(1.0)
        print("[INFO] Initialization complete. Starting main video loop.")

        sentence, live_prediction, last_spoken_prediction, last_prediction_for_sentence = "", "", "", ""
        prediction_buffer = []
        BUFFER_SIZE, STABILITY_THRESHOLD = 20, 0.8
        current_prediction = "blank"

        # --- Main Loop ---
        while True:
            ret, frame = cap.read()
            if not ret:
                print("[WARNING] Could not read a frame from the camera. Ending session.")
                break

            frame = cv2.flip(frame, 1)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(frame_rgb)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                    h, w, _ = frame.shape
                    x_coords = [landmark.x for landmark in hand_landmarks.landmark]
                    y_coords = [landmark.y for landmark in hand_landmarks.landmark]
                    
                    x_min, x_max = int(min(x_coords) * w), int(max(x_coords) * w)
                    y_min, y_max = int(min(y_coords) * h), int(max(y_coords) * h)
                    
                    padding = 30
                    x_min, y_min = max(0, x_min - padding), max(0, y_min - padding)
                    x_max, y_max = min(w, x_max + padding), min(h, y_max + padding)

                    cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
                    
                    hand_roi = frame[y_min:y_max, x_min:x_max]
                    
                    if hand_roi.size > 0:
                        gray_roi = cv2.cvtColor(hand_roi, cv2.COLOR_BGR2GRAY)
                        resized_roi = cv2.resize(gray_roi, (128, 128))
                        normalized_roi = resized_roi / 255.0
                        prediction = predict_sign(model, normalized_roi)
                        if prediction:
                            current_prediction = prediction
                            live_prediction = prediction
            else:
                current_prediction = "blank"

            prediction_buffer.append(current_prediction)
            if len(prediction_buffer) > BUFFER_SIZE: prediction_buffer.pop(0)
            
            if len(prediction_buffer) == BUFFER_SIZE:
                stable_prediction = max(set(prediction_buffer), key=prediction_buffer.count)
                stability = prediction_buffer.count(stable_prediction) / BUFFER_SIZE

                if stability >= STABILITY_THRESHOLD and stable_prediction != 'blank':
                    if stable_prediction != last_spoken_prediction:
                        speak(stable_prediction)
                        last_spoken_prediction = stable_prediction
                    if stable_prediction != last_prediction_for_sentence:
                        sentence += stable_prediction
                        last_prediction_for_sentence = stable_prediction
                else:
                    last_spoken_prediction, last_prediction_for_sentence = "", ""

            cv2.putText(frame, f"Sentence: {sentence}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(frame, f"Prediction: {live_prediction}", (20, frame.shape[0] - 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.imshow('Mook Mitra - MediaPipe Hand Tracking', frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'): break
            elif key == ord('s'): sentence += " "; speak("space")
            elif key == ord('c'):
                sentence, live_prediction, last_spoken_prediction, last_prediction_for_sentence = "", "", "", ""
                prediction_buffer.clear(); speak("cleared")

    except Exception as e:
        print(f"[ERROR] An unexpected error occurred in the camera loop: {e}")
        return f"Runtime error: {e}"
    finally:
        print("[INFO] Releasing camera and closing all windows.")
        if hands:
            hands.close()
        if cap:
            cap.release()
        cv2.destroyAllWindows()
    
    return sentence

