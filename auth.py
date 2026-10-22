import hashlib
import hmac
import os

from db import add_user, get_user


def hash_password(password):
    salt = os.urandom(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        600000
    )

    return salt.hex() + "$" + password_hash.hex()


def verify_password(password, stored_hash):
    try:
        salt_hex, hash_hex = stored_hash.split("$")

        salt = bytes.fromhex(salt_hex)

        password_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            600000
        )

        return hmac.compare_digest(
            password_hash.hex(),
            hash_hex
        )

    except (ValueError, TypeError):
        return False


def signup_user(name, email, password):
    existing_user = get_user(email)

    if existing_user is not None:
        return False

    password_hash = hash_password(password)

    return add_user(name, email, password_hash)


def login_user(email, password):
    user = get_user(email)

    if user is None:
        return None

    stored_hash = user[3]

    if verify_password(password, stored_hash):
        return {
            "id": user[0],
            "name": user[1],
            "email": user[2]
        }

    return None