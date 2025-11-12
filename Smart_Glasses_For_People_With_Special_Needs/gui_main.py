# Mook Mitra - Main GUI
import customtkinter
import threading
from camera_handler import start_camera
from speech_recognition_handler import listen_and_recognize

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Mook Mitra - Sign Language Assistant")
        self.geometry("800x600")
        customtkinter.set_appearance_mode("System")
        customtkinter.set_default_color_theme("blue")

        # --- Main Frame ---
        self.main_frame = customtkinter.CTkFrame(self)
        self.main_frame.pack(pady=20, padx=60, fill="both", expand=True)

        # --- Title Label ---
        self.title_label = customtkinter.CTkLabel(self.main_frame, text="Mook Mitra", font=customtkinter.CTkFont(size=40, weight="bold"))
        self.title_label.pack(pady=40, padx=10)

        # --- Description Label ---
        self.description_label = customtkinter.CTkLabel(self.main_frame, text="Your AI-Powered Sign Language Companion", font=customtkinter.CTkFont(size=16))
        self.description_label.pack(pady=10, padx=10)

        # --- Button Frame ---
        self.button_frame = customtkinter.CTkFrame(self.main_frame, fg_color="transparent")
        self.button_frame.pack(pady=50)

        # --- Start Camera Button ---
        self.camera_button = customtkinter.CTkButton(self.button_frame, text="Start Sign Language Detection", width=300, height=50, font=customtkinter.CTkFont(size=16), command=self.start_camera_thread)
        self.camera_button.pack(pady=15)
        
        # --- Start Voice Command Button ---
        self.voice_button = customtkinter.CTkButton(self.button_frame, text="Give Voice Command", width=300, height=50, font=customtkinter.CTkFont(size=16), command=self.start_voice_thread)
        self.voice_button.pack(pady=15)
        
        # --- Exit Button ---
        self.exit_button = customtkinter.CTkButton(self.main_frame, text="Exit", width=150, height=40, fg_color="red", hover_color="#C10000", command=self.quit_app)
        self.exit_button.pack(pady=20, side="bottom")

    def start_camera_thread(self):
        """ Runs the camera in a separate thread to prevent the GUI from freezing. """
        print("[GUI INFO] Starting camera thread...")
        camera_thread = threading.Thread(target=start_camera, daemon=True)
        camera_thread.start()
        
    def start_voice_thread(self):
        """ Runs the voice recognition in a separate thread. """
        print("[GUI INFO] Starting voice recognition thread...")
        voice_thread = threading.Thread(target=listen_and_recognize, daemon=True)
        voice_thread.start()
        
    def quit_app(self):
        """ Closes the application. """
        print("[GUI INFO] Exit button clicked. Closing application.")
        self.destroy()

if __name__ == "__main__":
    app = App()
    app.mainloop()