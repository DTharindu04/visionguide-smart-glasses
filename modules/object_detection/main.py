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
speech_cooldown = 4.0   # Wait 4 seconds before speaking again
FACE_CHECK_INTERVAL = 5 # Run face recognition every 5 frames
FRAME_WIDTH = 640 
FRAME_HEIGHT = 640

# --- CLASS: SMOOTHING (STABILIZER) ---
class SmoothTracker:
    def __init__(self):
        # Stores the history of positions to calculate average
        self.history = {} 

    def get_smooth_box(self, object_id, x1, y1, x2, y2):
        """
        Averages coordinates over 5 frames to stop the box from shaking.
        """
        center_x = (x1 + x2) / 2
        
        if object_id not in self.history:
            self.history[object_id] = []
        
        # Save current box to history
        self.history[object_id].append((center_x, x1, y1, x2, y2))
        
        # Keep only the last 5 frames
        if len(self.history[object_id]) > 5:
            self.history[object_id].pop(0)
            
        # Calculate Average Position
        avg_cx = sum(p[0] for p in self.history[object_id]) / len(self.history[object_id])
        avg_x1 = int(sum(p[1] for p in self.history[object_id]) / len(self.history[object_id]))
        avg_y1 = int(sum(p[2] for p in self.history[object_id]) / len(self.history[object_id]))
        avg_x2 = int(sum(p[3] for p in self.history[object_id]) / len(self.history[object_id]))
        avg_y2 = int(sum(p[4] for p in self.history[object_id]) / len(self.history[object_id]))
        
        return avg_cx, avg_x1, avg_y1, avg_x2, avg_y2

# --- AUDIO ENGINE ---
def speak_async(text):
    def _speak():
        try:
            engine = pyttsx3.init()
            engine.setProperty('rate', 160) # Speed of voice
            engine.say(text)
            engine.runAndWait()
        except: pass
    thread = threading.Thread(target=_speak)
    thread.start()
    print(f"🎤 SYSTEM: {text}")

# --- NAVIGATION LOGIC ---
def get_position(x_center):
    """
    Returns position with 'Buffer Zones' to prevent flickering.
    Left: < 220 | Center: 220-420 | Right: > 420
    """
    if x_center < 220: return "on Left"
    elif x_center > 420: return "on Right"
    else: return "Ahead"

# Motion Tracking Memory
last_positions = {}

def get_motion(label, current_x, current_y):
    """Determines if object is Moving or Stationary"""
    prev = last_positions.get(label)
    last_positions[label] = (current_x, current_y)
    
    if prev:
        # Check how many pixels it moved
        movement = abs(current_x - prev[0]) + abs(current_y - prev[1])
        if movement > 5: # Sensitivity threshold
            return "Moving"
    return "Stationary"

def estimate_distance(box_height):
    """Height-based distance warning"""
    if box_height > 350: return "Very Close!"
    elif box_height > 150: return "Near"
    else: return ""

# --- MAIN PROGRAM ---
def main():
    cap = cv2.VideoCapture(0)
    
    # Initialize AI Modules
    try:
        print("Initializing AI Systems...")
        detector = ObjectDetector()
        recognizer = FaceRecognizer()
        tracker = SmoothTracker()
    except Exception as e:
        print(f"🔴 Startup Error: {e}")
        return

    # Logging Setup (For Thesis Graphs)
    if LOG_DATA:
        filename = f"benchmark_log_{datetime.now().strftime('%H-%M')}.csv"
        log_file = open(filename, mode='w', newline='')
        writer = csv.writer(log_file)
        writer.writerow(["Time", "FPS", "Detections"])

    last_speech_time = 0
    frame_count = 0 
    current_names = {}
    
    print("✅ System Online. Press 'q' to exit.")
    speak_async("Vision Guide Active.")
    
    start_time = time.time()
    prev_frame_time = 0

    while True:
        ret, frame = cap.read()
        if not ret: break
        
        frame = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT))
        frame_count += 1
        
        # 1. DETECT OBJECTS
        results, detected_df = detector.detect(frame)
        annotated_frame = frame.copy()
        
        warnings = []
        
        # 2. PROCESS EACH OBJECT
        for index, row in detected_df.iterrows():
            # Get Raw Coordinates
            x1, y1, x2, y2 = int(row['xmin']), int(row['ymin']), int(row['xmax']), int(row['ymax'])
            label = row['name']
            
            # ID for smoothing
            obj_id = f"{label}_{index}" 
            
            # --- APPLY SMOOTHING ---
            smooth_cx, sx1, sy1, sx2, sy2 = tracker.get_smooth_box(obj_id, x1, y1, x2, y2)
            
            # Calculate Dimensions
            w_box = sx2 - sx1
            h_box = sy2 - sy1
            
            # --- FILTER: Aspect Ratio (Ghost Check) ---
            # If box is square (ratio < 1.1), it's likely not a person
            if label == 'person' and (h_box / w_box) < 1.1:
                continue 

            # --- GET SPATIAL DATA ---
            pos_msg = get_position(smooth_cx)
            dist_msg = estimate_distance(h_box)
            motion_msg = get_motion(label, smooth_cx, (sy1+sy2)/2)
            
            # --- FACE RECOGNITION LOGIC ---
            person_key = f"{int(sx1)//50}_{int(sy1)//50}" # Approximate ID location
            color = (255, 0, 0) # Blue (Default)
            
            if label == 'person':
                # Only check faces every 5 frames to save speed
                if frame_count % FACE_CHECK_INTERVAL == 0:
                    name = recognizer.recognize(frame, sx1, sy1, w_box, h_box)
                    if name and name != "Unknown":
                        current_names[person_key] = name
                
                # Check if we know this person
                display_name = current_names.get(person_key, "Person")
                if display_name != "Person":
                    label = display_name
                    color = (0, 255, 0) # Green for Friends
                    motion_msg = "" # Skip "Moving" for known friends
                else:
                    color = (0, 0, 255) # Red for Strangers

            # --- BUILD AUDIO WARNING ---
            # Only warn if object is "Near" or "Very Close"
            if dist_msg != "":
                full_msg = f"{motion_msg} {label} {pos_msg} {dist_msg}"
                warnings.append(full_msg)
                # Draw thick red box for danger
                cv2.rectangle(annotated_frame, (sx1, sy1), (sx2, sy2), (0, 0, 255), 3)
            else:
                # Draw normal box
                cv2.rectangle(annotated_frame, (sx1, sy1), (sx2, sy2), color, 2)
            
            # Draw Label
            caption = f"{label} {dist_msg}"
            cv2.putText(annotated_frame, caption, (sx1, sy1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        # 3. CALCULATE FPS
        new_frame_time = time.time()
        fps = 1 / (new_frame_time - prev_frame_time) if (new_frame_time - prev_frame_time) > 0 else 30
        prev_frame_time = new_frame_time
        
        # Log to CSV
        if LOG_DATA and time.time() - start_time > 2:
            writer.writerow([round(time.time()-start_time, 2), round(fps, 1), str(warnings)])

        # 4. SPEAK PRIORITY MESSAGE
        current_time = time.time()
        if warnings and (current_time - last_speech_time > speech_cooldown):
            speak_async(warnings[0])
            last_speech_time = current_time

        # 5. DRAW VISUAL GUIDES (Lines for Left/Center/Right)
        cv2.line(annotated_frame, (220, 0), (220, FRAME_HEIGHT), (100,100,100), 1)
        cv2.line(annotated_frame, (420, 0), (420, FRAME_HEIGHT), (100,100,100), 1)
        cv2.putText(annotated_frame, f"FPS: {int(fps)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        cv2.imshow('VisionGuide Prototype', annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    if LOG_DATA: log_file.close()

if __name__ == "__main__":
    main()