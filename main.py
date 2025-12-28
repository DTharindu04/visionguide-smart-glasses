import cv2
import pyttsx3
import threading
import time
import csv
from datetime import datetime
from detection import ObjectDetector
from recognition import FaceRecognizer

# --- CONFIGURATION ---
LOG_DATA = True       
speech_cooldown = 4.0 
FACE_CHECK_INTERVAL = 5 
FRAME_WIDTH = 640 # The width of our image
FRAME_HEIGHT = 640

# --- AUDIO ---
def speak_async(text):
    def _speak():
        try:
            engine = pyttsx3.init()
            engine.setProperty('rate', 160) # Speak slightly faster for warnings
            engine.say(text)
            engine.runAndWait()
        except: pass
    thread = threading.Thread(target=_speak)
    thread.start()
    print(f"🎤 SYSTEM: {text}")

# --- INIT ---
cap = cv2.VideoCapture(0)
detector = ObjectDetector()
recognizer = FaceRecognizer()

def get_position_label(x_center):
    """Tell the user if the object is Left, Center, or Right."""
    if x_center < FRAME_WIDTH / 3:
        return "on your Left"
    elif x_center > (FRAME_WIDTH / 3 * 2):
        return "on your Right"
    else:
        return "in Front"

def estimate_distance(box_height, label):
    """
    Guess distance based on how tall the object looks in pixels.
    This is a rough approximation for the thesis.
    """
    # Heuristic: A person closer than 1 meter usually fills 80% of the screen height (approx 500px)
    if box_height > 350:
        return "Very Close!"
    elif box_height > 150:
        return "Near"
    else:
        return "" # Too far to worry about

def main():
    last_speech_time = 0
    frame_count = 0 
    current_names = {}
    
    print("Navigation System Online.")
    speak_async("Navigation Mode Active.")
    
    while True:
        ret, frame = cap.read()
        if not ret: break
        
        frame = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT))
        frame_count += 1

        # 1. DETECT
        results, detected_df = detector.detect(frame)
        annotated_frame = frame.copy()
        
        warnings = [] # List of urgent things to say
        
        # 2. PROCESS OBJECTS
        for index, row in detected_df.iterrows():
            x1, y1, x2, y2 = int(row['xmin']), int(row['ymin']), int(row['xmax']), int(row['ymax'])
            label = row['name']
            
            # Calculate Center and Height for Navigation
            x_center = (x1 + x2) / 2
            box_height = y2 - y1
            
            position = get_position_label(x_center)
            distance_msg = estimate_distance(box_height, label)
            
            person_id = f"{x1 // 50}_{y1 // 50}" 
            color = (255, 0, 0)
            
            # FACE LOGIC
            if label == 'person':
                if frame_count % FACE_CHECK_INTERVAL == 0:
                    w = x2 - x1
                    h = y2 - y1
                    name = recognizer.recognize(frame, x1, y1, w, h)
                    if name and name != "Unknown":
                        current_names[person_id] = name
                
                display_name = current_names.get(person_id, "Person")
                if display_name != "Person":
                    label = display_name
                    color = (0, 0, 255)
                
            # 3. BUILD NAVIGATION MESSAGE
            # Only warn if the object is "Near" or "Very Close"
            if distance_msg != "":
                # Example: "Chair in Front Near" or "Pulasthi on your Right Very Close"
                warnings.append(f"{label} {position} {distance_msg}")
                # Draw Red Warning Box
                cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 0, 255), 3)
            else:
                cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), color, 2)

            cv2.putText(annotated_frame, f"{label} {distance_msg}", (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

        # 4. AUDIO PRIORITY SYSTEM
        current_time = time.time()
        if warnings and (current_time - last_speech_time > speech_cooldown):
            # Pick the most urgent warning (the first one)
            message = warnings[0] 
            speak_async(message)
            last_speech_time = current_time

        # 5. VISUALIZATION ZONES (Draw lines for Left/Center/Right)
        cv2.line(annotated_frame, (int(FRAME_WIDTH/3), 0), (int(FRAME_WIDTH/3), FRAME_HEIGHT), (100, 100, 100), 1)
        cv2.line(annotated_frame, (int(FRAME_WIDTH/3*2), 0), (int(FRAME_WIDTH/3*2), FRAME_HEIGHT), (100, 100, 100), 1)
        
        cv2.imshow('Smart Glasses Navigation', annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()