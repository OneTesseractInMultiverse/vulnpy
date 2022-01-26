import hashlib
import random
import re
from pathlib import Path
from time import time

import jwt
import libuser

secret = "MYSUPERSECRETKEY"
not_after = 60  # 1 minute


def keygen(username, password=None, login=True):

    if login:
        if not libuser.login(username, password):
            return None

    now = time()
    token = jwt.encode(
        {
            "username": username,
            "nbf": now,
            "exp": now + not_after
        },
        secret,
        algorithm="HS256",
    ).decode()

    return token


def authenticate(request):

    if "authorization" not in request.headers:
        return None

    try:
        authtype, token = request.headers["authorization"].split(" ")
    except Exception as e:
        print(e)
        return None

    if authtype.lower() != "bearer":
        print("not bearer")
        return None

    try:
        decoded = jwt.decode(token, secret, algorithms=["HS256"])
    except Exception as e:
        print(e)
        return None

    return decoded["username"]
