# Mook Mitra - Camera Diagnostic Tool
# This simple script helps to find the correct camera index and test its connection.

import cv2
import sys

def test_camera(index):
    """Attempts to open a camera at a given index and display the feed."""
    
    print(f"\n--- Testing Camera Index: {index} ---")
    
    # Attempt to open the camera using the DSHOW backend for Windows stability
    cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
    
    if not cap.isOpened():
        print(f"[RESULT] FAILED: Could not open camera at index {index}.")
        return False

    print(f"[RESULT] SUCCESS: Camera at index {index} opened.")
    print("A window should appear with your camera feed.")
    print("Press 'q' in the window to close it and finish the test.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[ERROR] Failed to read a frame from the camera. The stream may have been interrupted.")
            break
            
        cv2.imshow(f'Camera Test (Index {index}) - Press Q to Quit', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()
    print(f"--- Test for Index {index} Finished ---")
    return True

if __name__ == "__main__":
    print("Starting camera diagnostic tool...")
    
    # By default, we test index 0. If you provide a number (e.g., python camera_test.py 1), it will test that number.
    start_index = 0
    if len(sys.argv) > 1:
        try:
            start_index = int(sys.argv[1])
        except ValueError:
            print(f"Invalid argument '{sys.argv[1]}'. Please provide a number (e.g., 0, 1, 2).")
            sys.exit(1)

    if not test_camera(start_index):
        print("\n[NEXT STEP] The test at the default index failed.")
        print("Trying to find a working camera by testing other indices (1, 2, 3)...")
        for i in range(1, 4):
            if test_camera(i):
                print(f"\n[CONCLUSION] A working camera was found at Index {i}.")
                print("Please remember this number for the final fix.")
                break
        else:
            print("\n[CONCLUSION] No working camera could be found at indices 0, 1, 2, or 3.")
            print("This indicates a deeper issue with your webcam drivers or permissions.")