import sqlite3

DB_NAME = "chat.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def init_db():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            question TEXT,

            answer TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
    """)

    conn.commit()
    conn.close()

def save_chat(question, answer):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO chat_history
        (question, answer)
        VALUES (?, ?)
        """,
        (question, answer)
    )

    conn.commit()
    conn.close()

def load_history():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            question,
            answer,
            created_at
        FROM chat_history
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows