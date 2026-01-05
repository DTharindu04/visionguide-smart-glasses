from mtcnn import MTCNN
import cv2

class FaceDetector:
    def __init__(self):
        self.detector = MTCNN()

    def detect_faces(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        detections = self.detector.detect_faces(rgb_frame)

        faces = []
        for det in detections:
            x, y, w, h = det['box']
            confidence = det['confidence']

            if confidence > 0.90:
                faces.append({
                    "box": (x, y, w, h),
                    "confidence": confidence
                })

        return faces
