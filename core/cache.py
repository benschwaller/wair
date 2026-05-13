import hashlib
import json
from pathlib import Path


CACHE_DIR = Path("workspace/cache")


def cache_key(value):
    return hashlib.md5(value.encode()).hexdigest()


def save_cache(key, data):
    path = CACHE_DIR / f"{key}.json"

    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def load_cache(key):
    path = CACHE_DIR / f"{key}.json"

    if not path.exists():
        return None

    with open(path) as f:
        return json.load(f)