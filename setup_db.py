import os
import sqlite3

from auth import hash_password
from db import DATABASE

DEMO_USERNAME = "alice"
DEMO_PASSWORD = os.environ.get("DEMO_PASSWORD")


def initialize_database():
    password_hash = hash_password(DEMO_PASSWORD)

    with sqlite3.connect(DATABASE) as connection:
        connection.execute("DROP TABLE IF EXISTS users")
        connection.execute(
            """
            CREATE TABLE users (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            )
            """
        )
        connection.execute(
            """
            INSERT INTO users (username, password_hash)
            VALUES (?, ?)
            """,
            (DEMO_USERNAME, password_hash),
        )


if __name__ == "__main__":
    initialize_database()
    print("Demo database created with an Argon2 password hash")
