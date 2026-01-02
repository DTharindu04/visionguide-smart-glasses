import cv2
import numpy as np
from modules.face_recognition.facenet_model import FaceNetModel

class FaceEmbedder:
    def __init__(self):
        self.facenet = FaceNetModel()

    def preprocess_face(self, frame, box):
        x, y, w, h = box

        face = frame[y:y+h, x:x+w]
        face = cv2.resize(face, (160, 160))
        face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)

        return face

    def generate_embedding(self, face_img):
        embedding = self.facenet.get_embedding(face_img)
        return embedding
