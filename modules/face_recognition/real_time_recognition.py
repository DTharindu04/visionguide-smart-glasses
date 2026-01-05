import cv2
from modules.face_recognition.face_detection import FaceDetector
from modules.face_recognition.face_embedding import FaceEmbedder
from modules.face_recognition.face_database import FaceDatabase
from modules.face_recognition.face_matching import FaceMatcher
from modules.audio_feedback.tts_engine import TTSEngine


def run_face_recognition():
    detector = FaceDetector()
    embedder = FaceEmbedder()
    database = FaceDatabase()
    matcher = FaceMatcher(threshold=0.75)
    tts = TTSEngine()

    cap = cv2.VideoCapture(0)

    UNKNOWN_LIMIT = 15
    unknown_counter = 0
    last_spoken = None

    print("[INFO] Real-time face recognition started")
    print("[INFO] Press 'q' to quit")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        faces = detector.detect_faces(frame)
        known_faces = database.get_average_embeddings()

        for face in faces:
            x, y, w, h = face["box"]
            face_img = frame[y:y+h, x:x+w]

            embedding = embedder.generate_embedding(face_img)
            if embedding is None:
                continue

            name, score = matcher.find_best_match(embedding, known_faces)

            # UNKNOWN HANDLING
            if name == "Unknown":
                unknown_counter += 1

                if unknown_counter == UNKNOWN_LIMIT and last_spoken != "Unknown":
                    tts.speak("Unknown person ahead")
                    last_spoken = "Unknown"
            else:
                unknown_counter = 0

                if name != last_spoken:
                    tts.speak(f"{name} in front of you")
                    last_spoken = name

            # DRAW UI
            color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)

            cv2.putText(
                frame,
                f"{name} ({score})",
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                color,
                2
            )

        # REQUIRED FOR CAMERA DISPLAY
        cv2.imshow("Smart Glasses - Face Recognition", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("[INFO] Recognition stopped")


if __name__ == "__main__":
    run_face_recognition()
