import hashlib
from datetime import datetime

def id_hash():
    unix_time = int(datetime.now().timestamp())
    hash = hashlib.sha1(str.encode(str(unix_time))).hexdigest()
    return hash