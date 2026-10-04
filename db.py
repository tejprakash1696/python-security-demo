import sqlite3

DATABASE = "users.db"


def get_user_by_username(username):
    with sqlite3.connect(DATABASE) as connection:
        connection.row_factory = sqlite3.Row

        row = connection.execute(
            """
            SELECT id, username, password_hash
            FROM users
            WHERE username = ?
            """,
            (username,),
        ).fetchone()

    return dict(row) if row else None
