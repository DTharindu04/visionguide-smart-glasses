import numpy as np
from scipy.spatial.distance import cosine

class FaceMatcher:
    def __init__(self, threshold=0.5):
        """
        threshold: similarity threshold (lower = stricter)
        Recommended range: 0.4 – 0.6
        """
        self.threshold = threshold

    def cosine_similarity(self, emb1, emb2):
        return 1 - cosine(emb1, emb2)

    def find_best_match(self, live_embedding, known_faces):
        """
        live_embedding: numpy array (128-D)
        known_faces: list of tuples -> [(name, embedding), ...]

        Returns:
            (matched_name, similarity_score) or ("Unknown", best_score)
        """

        best_score = -1
        best_name = "Unknown"

        for name, stored_embedding in known_faces:
            score = self.cosine_similarity(live_embedding, stored_embedding)

            if score > best_score:
                best_score = score
                best_name = name

        if best_score >= self.threshold:
            return best_name, round(best_score, 3)
        else:
            return "Unknown", round(best_score, 3)
