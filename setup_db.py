import sqlite3

from db import DATABASE

DEMO_USERNAME = "alice"
DEMO_PASSWORD = "AlicePassword123!"


def initialize_database():
    with sqlite3.connect(DATABASE) as connection:
        connection.execute("DROP TABLE IF EXISTS users")

        connection.execute(
            """
            CREATE TABLE users (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
            """
        )

        connection.execute(
            """
            INSERT INTO users (username, password)
            VALUES (?, ?)
            """,
            (DEMO_USERNAME, DEMO_PASSWORD),
        )


if __name__ == "__main__":
    initialize_database()
    print("Demo database created")
