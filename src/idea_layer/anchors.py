import os, json, hashlib, time
from pathlib import Path
from typing import Dict, Tuple, List

ROOT = Path("transparency")
LOG = ROOT / "log.jsonl"
STATE = ROOT / "STATE.json"

def _ensure_dirs():
    ROOT.mkdir(parents=True, exist_ok=True)
    if not LOG.exists(): LOG.write_text("", encoding="utf-8")
    if not STATE.exists(): STATE.write_text(json.dumps({"n":0,"root":None}), encoding="utf-8")

def _entry_hash(data: dict) -> str:
    raw = json.dumps(data, sort_keys=True, separators=(",",":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()

def _merkle_root(hashes: List[str]) -> str:
    if not hashes: return None
    layer = [bytes.fromhex(h) for h in hashes]
    while len(layer) > 1:
        nxt = []
        for i in range(0, len(layer), 2):
            a = layer[i]
            b = layer[i+1] if i+1 < len(layer) else a
            nxt.append(hashlib.sha256(a + b).digest())
        layer = nxt
    return layer[0].hex()

def anchor_local(payload: dict) -> Dict:
    _ensure_dirs()
    h = _entry_hash(payload)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps({"ts": int(time.time()), "hash": h}) + "\n")

    # recompute root (simple; ok for small logs)
    hashes = [json.loads(line)["hash"] for line in LOG.read_text(encoding="utf-8").splitlines() if line.strip()]
    root = _merkle_root(hashes)
    state = {"n": len(hashes), "root": root}
    STATE.write_text(json.dumps(state, indent=2), encoding="utf-8")

    return {"type":"local", "log_index": state["n"]-1, "root": root}
