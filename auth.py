from db import get_user_by_username


def authenticate(username, password):
    user = get_user_by_username(username)

    if not user:
        return False

    return user["password"] == password
