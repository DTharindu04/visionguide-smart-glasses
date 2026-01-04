import cv2
from modules.face_recognition.face_detection import FaceDetector
from modules.face_recognition.face_embedding import FaceEmbedder
from modules.face_recognition.face_database import FaceDatabase
from modules.face_recognition.face_matching import FaceMatcher


def run_face_recognition():
    detector = FaceDetector()
    embedder = FaceEmbedder()
    database = FaceDatabase()
    matcher = FaceMatcher(threshold=0.75)

    cap = cv2.VideoCapture(0)

    print("[INFO] Real-time face recognition started")
    print("[INFO] Press 'q' to quit")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        faces = detector.detect_faces(frame)

        # Load database embeddings
        known_faces = database.get_all_faces()

        for face in faces:
            x, y, w, h = face["box"]
            face_img = frame[y:y+h, x:x+w]

            embedding = embedder.generate_embedding(face_img)
            if embedding is None:
                continue

            name, score = matcher.find_best_match(embedding, known_faces)

            # Draw bounding box
            color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)

            label = f"{name} ({score})"
            cv2.putText(
                frame,
                label,
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                color,
                2
            )

            # 👉 Later: send `name` to TTS module
            # audio_engine.speak(name)

        cv2.imshow("Smart Glasses - Face Recognition", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("[INFO] Recognition stopped")


if __name__ == "__main__":
    run_face_recognition()
