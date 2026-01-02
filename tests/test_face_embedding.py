import cv2
import sys
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(PROJECT_ROOT)

from modules.face_recognition.camera import Camera
from modules.face_recognition.face_detection import FaceDetector
from modules.face_recognition.face_embedding import FaceEmbedder

camera = Camera()
detector = FaceDetector()
embedder = FaceEmbedder()

while True:
    frame = camera.get_frame()
    if frame is None:
        break

    faces = detector.detect_faces(frame)

    for face in faces:
        x, y, w, h = face["box"]
        face_img = embedder.preprocess_face(frame, (x, y, w, h))
        embedding = embedder.generate_embedding(face_img)

        print("Embedding length:", len(embedding))
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    cv2.imshow("FaceNet Embedding Test", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
