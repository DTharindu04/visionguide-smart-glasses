import numpy as np
from scipy.spatial.distance import cosine


class FaceMatcher:
    def __init__(self, threshold=0.75, min_margin=0.05):
        """
        threshold   : minimum similarity to accept a match
        min_margin  : gap between best and second-best match
        """
        self.threshold = threshold
        self.min_margin = min_margin

    def cosine_similarity(self, emb1, emb2):
        return 1 - cosine(emb1, emb2)

    def find_best_match(self, query_embedding, known_faces):
        """
        known_faces: list of (name, embedding)
        """
        scores = []

        for name, emb in known_faces:
            score = self.cosine_similarity(query_embedding, emb)
            scores.append((name, score))

        if len(scores) == 0:
            return "Unknown", 0.0

        scores.sort(key=lambda x: x[1], reverse=True)

        best_name, best_score = scores[0]
        second_score = scores[1][1] if len(scores) > 1 else 0

        # Decision logic
        if best_score >= self.threshold and (best_score - second_score) >= self.min_margin:
            return best_name, round(best_score, 3)
        else:
            return "Unknown", round(best_score, 3)
