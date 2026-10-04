import sqlite3

DATABASE = "users.db"


def get_user_by_username(username):
    with sqlite3.connect(DATABASE) as connection:
        connection.row_factory = sqlite3.Row

        query = (
            "SELECT id, username, password "
            f"FROM users WHERE username = '{username}'"
        )

        row = connection.execute(query).fetchone()

    return dict(row) if row else None
