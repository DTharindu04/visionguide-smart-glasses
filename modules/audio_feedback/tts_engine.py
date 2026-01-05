import pyttsx3
import threading

class TTSEngine:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 160)

    def speak(self, text):
        threading.Thread(target=self._speak, args=(text,), daemon=True).start()

    def _speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()
