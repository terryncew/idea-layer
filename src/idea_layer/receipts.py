import json, time
from typing import Dict, Any
from .ids import make_ulid
from .crypto import privacy_bins, rotating_pepper, make_privacy_hmac, sign_object_hmac

SCHEMA_VER = "idea_layer/v0.1"

def now_iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

def make_ir(idea_uuid: str, creator_anon_id: str, *,
            idea_text_len: int,
            idea_summary_text: str,
            prompt_text: str,
            kappa: float,
            delta_hol: Dict[str, float],
            ucr: float,
            cycles: int,
            contradictions: int,
            guard_failures: list,
            plausibility_p: float,
            novelty_bucket: str,
            license_scope: str,
            consent_version: str,
            retention_days: int,
            privacy_secret: bytes,
            privacy_pepper: bytes) -> Dict[str, Any]:

    ir = {
      "schema_version": SCHEMA_VER,
      "receipt_id": make_ulid(),
      "idea_id": idea_uuid,
      "creator_anon_id": creator_anon_id,
      "privacy": {
        "idea_hmac": make_privacy_hmac(privacy_secret, idea_summary_text, privacy_pepper),
        "prompt_hmac": make_privacy_hmac(privacy_secret, prompt_text, privacy_pepper),
        "len_bin": privacy_bins(idea_text_len)
      },
      "signals": {
        "kappa": float(kappa),
        "delta_hol": {
          "prompt": float(delta_hol.get("prompt",0.0)),
          "tool": float(delta_hol.get("tool",0.0)),
          "retrieval": float(delta_hol.get("retrieval",0.0)),
          "model": float(delta_hol.get("model",0.0)),
          "cache": float(delta_hol.get("cache",0.0))
        },
        "ucr": float(ucr),
        "cycles": int(cycles),
        "contradictions": int(contradictions),
        "guard_failures": guard_failures or ["none"]
      },
      "priors": {
        "plausibility_p": float(plausibility_p),
        "novelty_bucket": str(novelty_bucket)
      },
      "policy": {
        "license": { "scope": license_scope },
        "consent": { "version": consent_version },
        "retention_days": int(retention_days)
      },
      "provenance": {
        "iat": now_iso(),
        "sig": { "alg":"hmac-sha256", "kid":"default", "sig":"" }
      }
    }
    return ir

def frontier_score(plausibility_p: float, E: float, k_hat: float) -> float:
    # F = P * (1 - E) * (1 - k̂)
    P = max(0.0, min(1.0, plausibility_p))
    Eh = max(0.0, min(1.0, E))
    kh = max(0.0, min(1.0, k_hat))
    return P * (1.0 - Eh) * (1.0 - kh)

def serialize_for_sig(obj: dict) -> bytes:
    # exclude the signature field itself
    tmp = json.loads(json.dumps(obj))
    prov = tmp.get("provenance", {})
    if "sig" in prov: prov.pop("sig", None)
    tmp["provenance"] = prov
    return json.dumps(tmp, sort_keys=True, separators=(",",":")).encode("utf-8")

def sign_receipt(obj: dict, key_id: str, key_bytes: bytes) -> dict:
    blob = serialize_for_sig(obj)
    obj["provenance"]["sig"] = sign_object_hmac(blob, key_id, key_bytes)
    return obj
