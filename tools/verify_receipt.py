import json, sys
from idea_layer.crypto import verify_object_hmac
from idea_layer.receipts import serialize_for_sig

def key_lookup(kid: str) -> bytes:
    # dev-only: single shared key via env; swap for real KMS/HSM
    import os
    return os.environ.get("IDEA_LAYER_HMAC_KEY","changeme-dev-key").encode("utf-8")

def main():
    if len(sys.argv) < 2:
        print("usage: python tools/verify_receipt.py path/to/receipt.json")
        sys.exit(1)
    obj = json.loads(open(sys.argv[1], "r", encoding="utf-8").read())
    sig = obj.get("provenance",{}).get("sig")
    if not sig: 
        print("no signature")
        sys.exit(2)
    ok = verify_object_hmac(serialize_for_sig(obj), sig, key_lookup)
    print("VALID" if ok else "INVALID")
    sys.exit(0 if ok else 3)

if __name__ == "__main__":
    main()
