# Mook Mitra - Enhanced Modern GUI (MediaPipe Version)
# FINAL, MOST STABLE VERSION: Uses a sequential approach to avoid concurrency deadlocks.

import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import threading
import os

# --- Backend handlers are imported only when needed ---

class MookMitraApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Mook Mitra (MediaPipe Enhanced)")
        self.geometry("1100x700")
        ctk.set_appearance_mode("light")

        # --- Color Palette & Configuration ---
        self.bg_color = "#F0F4F8"
        self.sidebar_color = "#E4E8EC"
        self.card_color = "#FFFFFF"
        self.button_color = "#00796B"
        self.cta_button_color = "#FFB74D"
        self.cta_hover_color = "#FFA726"
        self.text_color = "#333333"
        self.subtitle_color = "#666666"
        self.configure(fg_color=self.bg_color)

        # --- Build UI ---
        self.create_sidebar()
        self.main_area = ctk.CTkFrame(self, corner_radius=20, fg_color=self.bg_color)
        self.main_area.pack(side="right", expand=True, fill="both", padx=20, pady=20)
        self.create_home_screen()
        
        # --- Safe Initialization ---
        self.after(100, self.center_window)
        self.after(200, self.play_welcome_message)

    def create_sidebar(self):
        sidebar = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color=self.sidebar_color)
        sidebar.pack(side="left", fill="y")
        logo = ctk.CTkLabel(sidebar, text="Mook Mitra", font=ctk.CTkFont(size=26, weight="bold"), text_color=self.button_color)
        logo.pack(pady=(30, 40), padx=20)
        nav_buttons = [
            ("🏠 Home", self.show_home),
            ("🤟 Sign → Speech (MP)", self.launch_sign_to_speech),
            ("🎤 Speech → Text", self.launch_speech_to_text),
            ("ℹ About", lambda: CTkMessagebox(title="About Mook Mitra", message="This version uses MediaPipe for enhanced hand detection.", icon="info", button_color=self.button_color)),
            ("❌ Exit", self.destroy),
        ]
        for text, cmd in nav_buttons:
            ctk.CTkButton(
                sidebar, text=text, corner_radius=8, height=45, font=ctk.CTkFont(size=14),
                fg_color="transparent", text_color=self.subtitle_color, hover_color="#D8DEE4",
                command=cmd, anchor="w"
            ).pack(pady=8, padx=20, fill="x")

    def create_home_screen(self):
        self.home_frame = ctk.CTkFrame(self.main_area, fg_color="transparent")
        self.home_frame.pack(expand=True, fill="both")
        header = ctk.CTkLabel(self.home_frame, text="Breaking Communication Barriers", font=ctk.CTkFont(size=36, weight="bold"), text_color=self.text_color)
        header.pack(pady=(30, 10))
        subtitle = ctk.CTkLabel(self.home_frame, text="Real-time, Offline Sign ↔ Speech ↔ Text Conversion", font=ctk.CTkFont(size=16), text_color=self.subtitle_color)
        subtitle.pack()
        features_frame = ctk.CTkFrame(self.home_frame, fg_color="transparent")
        features_frame.pack(expand=True, fill="both", padx=20, pady=20)
        features_frame.grid_columnconfigure((0, 1), weight=1)
        features_frame.grid_rowconfigure(0, weight=1)
        sign_card = ctk.CTkFrame(features_frame, corner_radius=15, fg_color=self.card_color, border_width=1, border_color="#D8DEE4")
        sign_card.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.create_card_content(
            parent=sign_card, icon="🤟", title="Sign Language to Speech",
            description="Uses MediaPipe for robust hand tracking and your Keras model for classification.",
            button_text="Launch Feature", button_command=self.launch_sign_to_speech
        )
        self.speech_card = ctk.CTkFrame(features_frame, corner_radius=15, fg_color=self.card_color, border_width=1, border_color="#D8DEE4")
        self.speech_card.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.reset_speech_card()

    def play_welcome_message(self):
        from text_to_speech_handler import speak
        self.launch_in_thread(speak, "Welcome to Mook Mitra", True)

    def create_card_content(self, parent, icon, title, description, button_text, button_command):
        icon_label = ctk.CTkLabel(parent, text=icon, font=ctk.CTkFont(size=50), text_color=self.text_color)
        icon_label.pack(pady=(30, 10))
        title_label = ctk.CTkLabel(parent, text=title, font=ctk.CTkFont(size=22, weight="bold"), text_color=self.text_color)
        title_label.pack(pady=10)
        desc_label = ctk.CTkLabel(parent, text=description, wraplength=300, justify="center", text_color=self.subtitle_color)
        desc_label.pack(pady=10, padx=20, expand=True)
        button = ctk.CTkButton(parent, text=button_text, corner_radius=10, height=45,
                               fg_color=self.cta_button_color, hover_color=self.cta_hover_color,
                               font=ctk.CTkFont(size=16, weight="bold"),
                               command=button_command)
        button.pack(pady=(20, 30))

    def center_window(self):
        self.update_idletasks()
        width, height = self.winfo_width(), self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def launch_in_thread(self, target_function, *args):
        thread = threading.Thread(target=target_function, args=args)
        thread.daemon = True
        thread.start()
        
    def show_home(self):
        print("Home button clicked.")

    def launch_sign_to_speech(self):
        """
        Launches the camera sequentially for maximum stability.
        Temporarily hides the GUI to prevent deadlocks.
        """
        from camera_handler_mediapipe import start_camera
        
        self.withdraw() # Hide the main window
        final_sentence = start_camera() # Run camera function directly (blocking)
        self.deiconify() # Bring the main window back
        
        self.handle_sign_to_speech_result(sentence=final_sentence)

    def handle_sign_to_speech_result(self, sentence):
        from text_to_speech_handler import speak
        if sentence and "not found" not in sentence and "error" not in sentence.lower():
            msg = f"The final detected sentence is:\n\n'{sentence}'"
            CTkMessagebox(title="Sentence Detected", message=msg, icon="check", button_color=self.button_color)
            self.launch_in_thread(speak, f"The final sentence is: {sentence}", True)
        else:
            CTkMessagebox(title="Info", message="No sentence was detected or the session was closed.", icon="info", button_color=self.button_color)

    def launch_speech_to_text(self):
        self.speech_title.configure(text="Listening...")
        self.speech_icon.configure(text="💬")
        self.speech_desc.configure(state="normal")
        self.speech_desc.delete("1.0", "end")
        self.speech_desc.insert("1.0", "Speak clearly into your microphone...\nThe result will appear here when you pause.")
        self.speech_desc.configure(state="disabled")
        self.speech_button.configure(state="disabled", text="Working...")
        self.launch_in_thread(self.run_and_show_result)

    def run_and_show_result(self):
        from speech_to_text_handler import listen_and_transcribe
        transcribed_text = listen_and_transcribe()
        self.after(100, self.update_ui_with_transcription, transcribed_text)

    def update_ui_with_transcription(self, text):
        from text_to_speech_handler import speak
        self.speech_title.configure(text="Transcription Complete")
        self.speech_icon.configure(text="✅")
        self.speech_desc.configure(state="normal")
        self.speech_desc.delete("1.0", "end")
        if text and "not found" not in text and "error" not in text.lower():
             self.speech_desc.insert("1.0", f"'{text}'")
             self.launch_in_thread(speak, f"You said: {text}", True)
        else:
            self.speech_desc.insert("1.0", "Could not understand audio or an error occurred.")
        self.speech_desc.configure(state="disabled", font=ctk.CTkFont(size=16, weight="bold"))
        self.speech_button.configure(state="normal", text="Start New Session", command=self.reset_speech_card)

    def reset_speech_card(self):
        for widget in self.speech_card.winfo_children():
            widget.destroy()
        self.speech_icon = ctk.CTkLabel(self.speech_card, text="🎤", font=ctk.CTkFont(size=50), text_color=self.text_color)
        self.speech_title = ctk.CTkLabel(self.speech_card, text="Speech to Text", font=ctk.CTkFont(size=22, weight="bold"), text_color=self.text_color)
        self.speech_desc = ctk.CTkTextbox(self.speech_card, wrap="word", height=80, fg_color="transparent",
                                          font=ctk.CTkFont(size=14), text_color=self.subtitle_color,
                                          activate_scrollbars=False)
        self.speech_desc.insert("1.0", "Transcribes spoken words from your microphone\ninto text using an offline engine.")
        self.speech_desc.configure(state="disabled")
        self.speech_button = ctk.CTkButton(self.speech_card, text="Launch Feature", corner_radius=10, height=45,
                                           fg_color=self.cta_button_color, hover_color=self.cta_hover_color,
                                           font=ctk.CTkFont(size=16, weight="bold"),
                                           command=self.launch_speech_to_text)
        self.speech_icon.pack(pady=(30, 10))
        self.speech_title.pack(pady=10)
        self.speech_desc.pack(pady=10, padx=20, expand=True)
        self.speech_button.pack(pady=(20, 30))

if __name__ == "__main__":
    if not os.path.exists('model'):
        root = ctk.CTk()
        root.withdraw()
        CTkMessagebox(title="Error", message="The 'model' directory containing the Keras model was not found.", icon="cancel")
        root.destroy()
    else:
        app = MookMitraApp()
        app.mainloop()

