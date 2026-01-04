import cv2
import numpy as np
from modules.face_recognition.face_detection import FaceDetector
from modules.face_recognition.face_embedding import FaceEmbedder
from modules.face_recognition.face_database import FaceDatabase


def enroll_person(person_name, num_samples=5):
    detector = FaceDetector()
    embedder = FaceEmbedder()
    database = FaceDatabase()

    cap = cv2.VideoCapture(0)
    embeddings = []

    print(f"[INFO] Enrolling face for: {person_name}")
    print("[INFO] Press 'c' to capture, 'q' to quit")

    while len(embeddings) < num_samples:
        ret, frame = cap.read()
        if not ret:
            break

        faces = detector.detect_faces(frame)

        # Draw detected faces
        for face in faces:
            x, y, w, h = face["box"]
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        cv2.imshow("Face Enrollment", frame)
        key = cv2.waitKey(1) & 0xFF

        # Capture only when user presses 'c'
        if key == ord('c'):
            if len(faces) == 0:
                print("[WARN] No face detected. Try again.")
                continue

            # Take first detected face
            x, y, w, h = faces[0]["box"]
            face_img = frame[y:y+h, x:x+w]

            embedding = embedder.generate_embedding(face_img)

            if embedding is None:
                print("[WARN] Embedding failed. Try again.")
                continue

            embeddings.append(embedding)
            print(f"[INFO] Sample {len(embeddings)}/{num_samples} captured")

            cv2.waitKey(400)  # avoid duplicate captures

        elif key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    # ---- AVERAGE & NORMALIZE ----
    if len(embeddings) == num_samples:
        avg_embedding = np.mean(embeddings, axis=0)
        avg_embedding = avg_embedding / np.linalg.norm(avg_embedding)

        database.add_face(person_name, avg_embedding)
        print("[INFO] Enrollment completed with averaged embedding.")
    else:
        print("[WARN] Enrollment incomplete. No data saved.")


if __name__ == "__main__":
    name = input("Enter person name: ")
    enroll_person(name)
