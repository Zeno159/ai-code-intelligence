import hashlib
import random
import string
from models import User


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def generate_token(length=32):
    chars = string.ascii_letters + string.digits
    return "".join(random.choice(chars) for _ in range(length))


def register_user(username, email, age, password):
    hashed = hash_password(password)
    user = User(username, email, age)
    token = generate_token()
    return {"user": user.get_profile(), "token": token, "password_hash": hashed}


def login(username, password, stored_hash):
    hashed = hash_password(password)
    if hashed == stored_hash:
        token = generate_token()
        return {"success": True, "token": token}
    return {"success": False, "token": None}


def logout(token, active_tokens):
    if token in active_tokens:
        active_tokens.remove(token)
        return True
    return False
