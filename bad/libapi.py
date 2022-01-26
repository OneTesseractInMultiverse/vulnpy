import hashlib
import random
from pathlib import Path

import libuser


def keygen(username, password=None):

    if password:
        if not libuser.login(username, password):
            return None

    key = hashlib.sha256(str(random.getrandbits(2048)).encode()).hexdigest()

    for f in Path("/tmp/").glob("vulpy.apikey." + username + ".*"):
        print("removing", f)
        f.unlink()

    keyfile = "/tmp/vulpy.apikey.{}.{}".format(username, key)

    Path(keyfile).touch()

    return key


def authenticate(request):
    if "X-APIKEY" not in request.headers:
        return None

    key = request.headers["X-APIKEY"]

    for f in Path("/tmp/").glob("vulpy.apikey.*." + key):
        return f.name.split(".")[2]

    return None
