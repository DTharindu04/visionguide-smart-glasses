import cv2
import time
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

    seen_names = set()
    last_audio_time = time.time()
    AUDIO_COOLDOWN = 3

    PROCESS_EVERY_N_FRAMES = 5
    frame_count = 0

    UNKNOWN_LIMIT = 15
    unknown_counter = 0

    prev_results = []

    known_faces = database.get_average_embeddings()

    print("[INFO] Face recognition started")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        current_time = time.time()   

        small_frame = cv2.resize(frame, None, fx=0.5, fy=0.5)

        if frame_count % PROCESS_EVERY_N_FRAMES == 0:
            faces = detector.detect_faces(small_frame)
            prev_results = []

            for face in faces:
                x, y, w, h = face["box"]
                x, y, w, h = [int(v * 2) for v in (x, y, w, h)]

                h_frame, w_frame = frame.shape[:2]
                x = max(0, x)
                y = max(0, y)
                w = min(w, w_frame - x)
                h = min(h, h_frame - y)

                if w <= 0 or h <= 0:
                    continue

                face_img = frame[y:y+h, x:x+w]
                embedding = embedder.generate_embedding(face_img)

                if embedding is None:
                    continue

                name, score = matcher.find_best_match(embedding, known_faces)
                prev_results.append((x, y, w, h, name, score))

        unknown_counter = 0  

        for x, y, w, h, name, score in prev_results:
            color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            cv2.putText(frame, f"{name} ({score})", (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

            if name == "Unknown":
                unknown_counter += 1
                if unknown_counter >= UNKNOWN_LIMIT and "Unknown" not in seen_names:
                    tts.speak("Unknown person ahead")
                    seen_names.add("Unknown")
            else:
                if name not in seen_names:
                    tts.speak(f"{name} in front of you")
                    seen_names.add(name)

        #  Clear spoken names every cooldown
        if current_time - last_audio_time > AUDIO_COOLDOWN:
            seen_names.clear()
            last_audio_time = current_time

        cv2.imshow("Smart Glasses - Face Recognition", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("[INFO] Recognition stopped")


if __name__ == "__main__":
    run_face_recognition() 
 