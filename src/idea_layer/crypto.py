import hmac, hashlib, base64
from typing import Tuple

def hmac_sha256(key: bytes, msg: bytes) -> str:
    return hmac.new(key, msg, hashlib.sha256).hexdigest()

def sign_object_hmac(obj_bytes: bytes, key_id: str, key_bytes: bytes) -> dict:
    sig = hmac.new(key_bytes, obj_bytes, hashlib.sha256).digest()
    return {"alg":"hmac-sha256", "kid": key_id, "sig": base64.b64encode(sig).decode("ascii")}

def verify_object_hmac(obj_bytes: bytes, sig: dict, key_lookup) -> bool:
    if sig.get("alg") != "hmac-sha256": return False
    kid = sig.get("kid"); raw = sig.get("sig")
    if not kid or not raw: return False
    key = key_lookup(kid)
    expect = hmac.new(key, obj_bytes, hashlib.sha256).digest()
    try:
        got = base64.b64decode(raw.encode("ascii"))
    except Exception:
        return False
    return hmac.compare_digest(expect, got)

def privacy_bins(length: int) -> str:
    if length <= 280: return "S"
    if length <= 1000: return "M"
    if length <= 5000: return "L"
    return "XL"

def rotating_pepper(day_epoch: int) -> bytes:
    # simple daily pepper derivation (swap with TOTP/HSM in prod)
    seed = f"pepper:{day_epoch}".encode()
    return hashlib.sha256(seed).digest()

def make_privacy_hmac(secret: bytes, text: str, pepper: bytes) -> str:
    return hmac_sha256(secret + pepper, text.encode("utf-8"))
