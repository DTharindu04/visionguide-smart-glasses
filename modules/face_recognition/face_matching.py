import numpy as np
from scipy.spatial.distance import cosine


class FaceMatcher:
    def __init__(self, threshold=0.75):
        """
        threshold: cosine similarity threshold
        Recommended:
        - FaceNet : 0.7 – 0.8
        """
        self.threshold = threshold

    def cosine_similarity(self, emb1, emb2):
        return 1 - cosine(emb1, emb2)

    def find_best_match(self, query_embedding, database_embeddings):
        """
        query_embedding: numpy array
        database_embeddings: list of (name, embedding)
        """

        best_name = "Unknown"
        best_score = -1

        for name, db_embedding in database_embeddings:
            score = self.cosine_similarity(query_embedding, db_embedding)

            if score > best_score:
                best_score = score
                best_name = name

        if best_score >= self.threshold:
            return best_name, round(best_score, 3)
        else:
            return "Unknown", round(best_score, 3)
