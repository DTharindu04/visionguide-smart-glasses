import sqlite3
import numpy as np
import os
from datetime import datetime

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

    # Enrollment
    
    def add_face(self, name, embedding):
        embedding_blob = embedding.tobytes()
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO faces (name, embedding, created_at)
            VALUES (?, ?, ?)
        """, (name, embedding_blob, datetime.now().isoformat()))
        conn.commit()
        conn.close()

    # Retrieve all faces

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

    # Delete a face

    def delete_face(self, name):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM faces WHERE name = ?", (name,))
        conn.commit()
        conn.close()

    # Check database size

    def count_faces(self):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM faces")
        count = cursor.fetchone()[0]
        conn.close()
        return count
