import hashlib


async def req_to_hash(req: str) -> str:
    hash_object = hashlib.sha256()
    hash_object.update(req.encode("utf-8"))
    hex_dig: str = hash_object.hexdigest()

    return hex_dig
