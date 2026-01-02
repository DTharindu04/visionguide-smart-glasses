import cv2
from modules.face_recognition.camera import Camera
from modules.face_recognition.face_detection import FaceDetector

camera = Camera()
detector = FaceDetector()

while True:
    frame = camera.get_frame()
    if frame is None:
        break

    faces = detector.detect_faces(frame)

    for face in faces:
        x, y, w, h = face["box"]
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    cv2.imshow("Face Detection - MTCNN", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
