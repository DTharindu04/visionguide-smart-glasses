import pyttsx3

# Initialize the speech engine
engine = pyttsx3.init()

# 1. Setup Voice Properties (Optional but good for testing)
# Speed of speech (default is usually around 200)
engine.setProperty('rate', 150)    
# Volume (0.0 to 1.0)
engine.setProperty('volume', 1.0)  

print("Testing Audio... Listen carefully.")

# 2. Queue the text to be spoken
engine.say("System initialized. Audio test successful.")

# 3. Process the voice commands
engine.runAndWait()

print("Did you hear that?")