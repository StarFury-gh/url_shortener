from core.config import cfg_obj
from jwt import encode, decode


def encode_token(payload: dict) -> str:
    jwt = encode(payload=payload, key=cfg_obj.JWT_SECRET_KEY, algorithm="HS256")
    return jwt


def decode_token(jwt: str) -> dict:
    payload = decode(jwt, key=cfg_obj.JWT_SECRET_KEY, algorithms=["HS256"])
    return payload
