import os, time, base64

# Minimal ULID-ish (time prefix + random) for readability, not strict ULID spec
def make_ulid() -> str:
    ts = int(time.time() * 1000).to_bytes(6, "big")
    rnd = os.urandom(10)
    b = ts + rnd
    return base64.b32encode(b).decode("ascii").rstrip("=").lower()
