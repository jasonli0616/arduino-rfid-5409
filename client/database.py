import sqlite3


class Database:
    def __init__(self):
        """Connect to the database, and create table."""

        self.connection = sqlite3.connect(
            "arduino-rfid-5409.db", check_same_thread=False
        )
        self.cursor = self.connection.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS users (uid, student_id)")

    def get_student_id(self, uid):
        """Return a student ID given the UID."""

        res = self.cursor.execute("SELECT student_id FROM users WHERE uid = ?", (uid,))
        return res.fetchone()

    def get_uid(self, student_id):
        """Return a UID given the student ID."""

        res = self.cursor.execute(
            "SELECT uid FROM users WHERE student_id = ?", (student_id,)
        )
        return res.fetchone()

    def create_new_user(self, uid, student_id):
        """Create a new user in the database."""

        self.cursor.execute(
            "INSERT INTO users VALUES (?, ?)",
            (
                uid,
                student_id,
            ),
        )
        self.connection.commit()
