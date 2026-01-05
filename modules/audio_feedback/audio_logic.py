import os
import pygame

class SmartGlassAudio:
    def __init__(self):
        self.base_path = "assets/audio"
        self.languages = ['si', 'en', 'ta', 'hi', 'ja', 'ko']
        self.current_lang = 'si'

    def set_language(self, lang_code):
        if lang_code in self.languages:
            self.current_lang = lang_code

    def play_feedback(self, label):
        file_path = os.path.join(self.base_path, self.current_lang, f"{label}.mp3")
        
        if os.path.exists(file_path):
            self._run_audio(file_path)
        else:
            print(f"Asset not found: {file_path}")

    def _run_audio(self, path):
        pygame.mixer.init()
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy(): continue
        pygame.mixer.quit()