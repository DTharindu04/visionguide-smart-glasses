import cv2
from modules.face_recognition.face_detection import FaceDetector
from modules.face_recognition.face_embedding import FaceEmbedder
from modules.face_recognition.face_database import FaceDatabase
from modules.face_recognition.face_matching import FaceMatcher


class FaceRecognitionPipeline:
    def __init__(self):
        self.detector = FaceDetector()
        self.embedder = FaceEmbedder()
        self.database = FaceDatabase()
        self.matcher = FaceMatcher(threshold=0.55)

    def process_frame(self, frame):
        """
        Input: BGR image frame
        Output: list of recognition results
        """

        results = []

        faces = self.detector.detect_faces(frame)

        if not faces:
            return results

        known_faces = self.database.get_all_faces()

        for face in faces:
            x, y, w, h = face["box"]
            face_img = frame[y:y+h, x:x+w]

            embedding = self.embedder.get_embedding(face_img)

            if embedding is None:
                continue

            name, confidence = self.matcher.find_best_match(
                embedding, known_faces
            )

            results.append({
                "name": name,
                "confidence": confidence,
                "box": (x, y, w, h)
            })

        return results
