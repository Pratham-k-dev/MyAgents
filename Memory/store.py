#store.py

import sqlite3
from pathlib import Path
from .schemas import Message
class SQLiteStore:

    def __init__(self, db_path: str):
        self.db_path = Path(db_path)

        # create parent directory if needed
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row

        self.initialize()

    def initialize(self):
        cursor = self.conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions(
            id TEXT PRIMARY KEY,
            summary TEXT DEFAULT '',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(session_id)
            REFERENCES sessions(id)
            ON DELETE CASCADE
        )
        """)

        self.conn.commit()

    def create_session(self, session_id: str):

        cursor = self.conn.cursor()

        cursor.execute(
            """
            INSERT INTO sessions(id)
            VALUES(?)
            """,
            (session_id,)
        )

        self.conn.commit()

    def load_session(self, session_id: str):

        cursor = self.conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM sessions
            WHERE id=?
            """,
            (session_id,)
        )

        return cursor.fetchone()

    def save_summary(
        self,
        session_id: str,
        summary: str
    ):

        cursor = self.conn.cursor()

        cursor.execute(
            """
            UPDATE sessions
            SET summary=?
            WHERE id=?
            """,
            (summary, session_id)
        )

        self.conn.commit()
    def get_summary(self, session_id: str):

        cursor = self.conn.cursor()

        cursor.execute(
            """
            SELECT summary
            FROM sessions
            WHERE id=?
            """,
            (session_id,)
        )

        row = cursor.fetchone()

        if row is None:
            return ""

        return row["summary"]

    def add_message(
    self,
    session_id: str,
    role: str,
    content: str
):

        cursor = self.conn.cursor()

        cursor.execute(
            """
            INSERT INTO messages(session_id, role, content)
            VALUES(?,?,?)
            """,
            (session_id, role, content)
        )

        self.conn.commit()

    def get_messages(self, session_id: str, limit: int | None = None):

        cursor = self.conn.cursor()

        if limit is None:
            cursor.execute(
                """
                SELECT *
                FROM messages
                WHERE session_id=?
                ORDER BY id ASC
                """,
                (session_id,)
            )

        else:
            cursor.execute(
                """
                SELECT *
                FROM (
                    SELECT *
                    FROM messages
                    WHERE session_id=?
                    ORDER BY id DESC
                    LIMIT ?
                )
                ORDER BY id ASC
                """,
                (session_id, limit)
            )

        rows = cursor.fetchall()

        return [
            Message(
                id=row["id"],
                session_id=row["session_id"],
                role=row["role"],
                content=row["content"],
                created_at=row["created_at"],
            )
            for row in rows
        ]
        

    def delete_messages(
        self,
        ids: list[int]
    ):

        if not ids:
            return

        cursor = self.conn.cursor()

        placeholders = ",".join("?" * len(ids))

        cursor.execute(
            f"""
            DELETE FROM messages
            WHERE id IN ({placeholders})
            """,
            ids
        )

        self.conn.commit()
    def close(self):
        self.conn.close()



