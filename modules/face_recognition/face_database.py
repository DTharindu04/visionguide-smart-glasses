import sqlite3
import numpy as np
import os
from datetime import datetime
import secrets

DB_PATH = "database/faces.db"

class FaceDatabase:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self._create_table()

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _create_table(self):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS faces (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                embedding BLOB NOT NULL,
                created_at TEXT
            )
        """)
        conn.commit()
        conn.close()

    
    #  ADD FACE (ENROLLMENT)
    
    def add_face(self, name, embedding):
        embedding_blob = embedding.astype(np.float32).tobytes()
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO faces (name, embedding, created_at)
            VALUES (?, ?, ?)
        """, (name, embedding_blob, datetime.now().isoformat()))
        conn.commit()
        conn.close()

   
    #  GET ALL FACES
   
    def get_all_faces(self):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT name, embedding FROM faces")
        rows = cursor.fetchall()
        conn.close()

        faces = []
        for name, emb_blob in rows:
            embedding = np.frombuffer(emb_blob, dtype=np.float32)
            faces.append((name, embedding))
        return faces

   
    #  AVERAGE EMBEDDINGS PER PERSON
   
    def get_average_embeddings(self):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT name, embedding FROM faces")
        rows = cursor.fetchall()
        conn.close()

        person_embeddings = {}

        for name, emb_blob in rows:
            emb = np.frombuffer(emb_blob, dtype=np.float32)
            person_embeddings.setdefault(name, []).append(emb)

        averaged_faces = []
        for name, embeddings in person_embeddings.items():
            avg_emb = np.mean(embeddings, axis=0)
            avg_emb = avg_emb / np.linalg.norm(avg_emb)  # normalize
            averaged_faces.append((name, avg_emb))

        return averaged_faces

    
    #  SECURE DELETE PERSON
   
    def secure_delete_person(self, name):
        conn = self._connect()
        cursor = conn.cursor()

        # Overwrite embeddings before deletion (secure erase)
        cursor.execute("SELECT id FROM faces WHERE name = ?", (name,))
        ids = cursor.fetchall()

        for (face_id,) in ids:
            random_blob = secrets.token_bytes(512)
            cursor.execute(
                "UPDATE faces SET embedding = ? WHERE id = ?",
                (random_blob, face_id)
            )

        cursor.execute("DELETE FROM faces WHERE name = ?", (name,))
        conn.commit()
        conn.close()

        print(f"[INFO] Securely deleted all data for '{name}'")

   
    #  UPDATE PERSON (RE-ENROLL)
   
    def update_person(self, name):
        self.secure_delete_person(name)
        print(f"[INFO] Ready to re-enroll '{name}'")

   
    #  DATABASE STATISTICS (EVALUATION)
   
    def count_faces(self):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM faces")
        count = cursor.fetchone()[0]
        conn.close()
        return count

    def count_identities(self):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(DISTINCT name) FROM faces")
        count = cursor.fetchone()[0]
        conn.close()
        return count
