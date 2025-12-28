import os
import cv2
import numpy as np
from deepface import DeepFace

class FaceRecognizer:
    def __init__(self):
        print("Loading Face Recognition System...")
        self.db_path = "faces" # Folder where you put your photos
        self.known_faces = []
        self.known_names = []
        
        # 1. Load all faces from the folder once at startup
        self.load_database()

    def load_database(self):
        """Loads images from the 'faces' folder to remember who people are."""
        if not os.path.exists(self.db_path):
            os.makedirs(self.db_path)
            print(f"Created '{self.db_path}' folder. Please put photos here!")
            return

        files = [f for f in os.listdir(self.db_path) if f.endswith(('.jpg', '.png'))]
        
        print(f"Found {len(files)} known faces in database.")
        
        # DeepFace uses the folder directly, but we do a quick check to make sure files exist
        for f in files:
            path = os.path.join(self.db_path, f)
            name = os.path.splitext(f)[0] # "pulasthi.jpg" -> "pulasthi"
            self.known_names.append(name)
            # We don't need to pre-load embeddings manually; DeepFace handles caching!

     
    def recognize(self, frame, x, y, w, h):
        try:
            # 1. Crop the person
            person_img = frame[y:y+h, x:x+w]
            
            # Check size
            if person_img.shape[0] < 50 or person_img.shape[1] < 50:
                print("⚠️ Face Rec: Image too small. Get closer.")
                return None

            # 2. Run DeepFace (Using 'opencv' again for now as it's safest)
            # We print "Checking..." so you know it's trying
            print(f"🔍 Checking face ({w}x{h})...")
            
            results = DeepFace.find(img_path=person_img, 
                                  db_path=self.db_path, 
                                  model_name="VGG-Face",
                                  detector_backend="opencv", # Safest backend
                                  enforce_detection=False, 
                                  silent=True)
            
            # 3. Check results
            if len(results) > 0 and not results[0].empty:
                matched_path = results[0].iloc[0]['identity']
                clean_name = os.path.basename(matched_path).split('.')[0]
                print(f"✅ MATCH FOUND: {clean_name}")
                return clean_name
            
            print("❌ Face not recognized (Unknown).")
            return "Unknown"

        except Exception as e:
            # THIS IS THE KEY: Print the actual error!
            print(f"🔴 ERROR in Face Rec: {e}")
            return None