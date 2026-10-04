from argon2 import PasswordHasher
from argon2.exceptions import VerificationError

from db import get_user_by_username

password_hasher = PasswordHasher()


def hash_password(password):
    return password_hasher.hash(password)


def authenticate(username, password):
    user = get_user_by_username(username)

    if not user:
        return False

    try:
        password_hasher.verify(
            user["password_hash"],
            password,
        )
        return True
    except VerificationError:
        return False
