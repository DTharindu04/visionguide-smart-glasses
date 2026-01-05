import numpy as np
from modules.face_recognition.face_database import FaceDatabase
from modules.face_recognition.face_matching import FaceMatcher


class ThresholdTuner:
    def __init__(self, thresholds=np.arange(0.3, 0.9, 0.02)):
        self.thresholds = thresholds
        self.db = FaceDatabase()

    def evaluate(self, known_faces):
        """
        Splits embeddings into genuine and impostor pairs
        """
        genuine_scores = []
        impostor_scores = []

        matcher = FaceMatcher()

        for i, (name1, emb1) in enumerate(known_faces):
            for j, (name2, emb2) in enumerate(known_faces):
                if i == j:
                    continue

                score = matcher.cosine_similarity(emb1, emb2)

                if name1 == name2:
                    genuine_scores.append(score)
                else:
                    impostor_scores.append(score)

        return np.array(genuine_scores), np.array(impostor_scores)

    def tune(self):
        known_faces = self.db.get_all_faces()

        if len(known_faces) < 2:
            print("[ERROR] Not enough data to tune threshold")
            return None

        genuine, impostor = self.evaluate(known_faces)

        best_threshold = None
        best_accuracy = 0

        for t in self.thresholds:
            true_accept = np.sum(genuine >= t)
            false_reject = np.sum(genuine < t)
            false_accept = np.sum(impostor >= t)
            true_reject = np.sum(impostor < t)

            accuracy = (true_accept + true_reject) / (
                len(genuine) + len(impostor)
            )

            if accuracy > best_accuracy:
                best_accuracy = accuracy
                best_threshold = t

        print(f"[RESULT] Best Threshold: {best_threshold:.2f}")
        print(f"[RESULT] Accuracy: {best_accuracy:.3f}")

        return best_threshold, best_accuracy


if __name__ == "__main__":
    tuner = ThresholdTuner()
    tuner.tune()
