import os
import time
import pygame
import pyttsx3

class SmartGlassAudio:
    def __init__(self):
        self.base_path = "assets/audio"
        self.languages = ['si', 'en', 'ta', 'hi', 'ja', 'ko']
        self.current_lang = 'si'

        # Initialize TTS engine
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)

    def set_language(self, lang_code):
        if lang_code in self.languages:
            self.current_lang = lang_code

    #  Existing: play prerecorded audio
    def play_feedback(self, label):
        file_path = os.path.join(
            self.base_path,
            self.current_lang,
            f"{label}.mp3"
        )

        if os.path.exists(file_path):
            self._run_audio(file_path)
        else:
            print(f"Asset not found: {file_path}")

    #  NEW: pygame TTS speak (replacement for tts.speak)
    def pygame_speak(self, text):
        temp_file = "temp_tts.wav"

        # Text → Speech
        self.engine.save_to_file(text, temp_file)
        self.engine.runAndWait()

        # Play with pygame
        self._run_audio(temp_file)

        # Cleanup
        if os.path.exists(temp_file):
            os.remove(temp_file)

    #  Shared audio runner
    def _run_audio(self, path):
        pygame.mixer.init()
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            time.sleep(0.05)

        pygame.mixer.quit()
