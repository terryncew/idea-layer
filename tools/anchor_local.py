import json, sys
from idea_layer.anchors import anchor_local
from pathlib import Path

def main():
    if len(sys.argv) < 2:
        print("usage: python tools/anchor_local.py path/to/receipt.json")
        sys.exit(1)
    path = Path(sys.argv[1])
    rec = json.loads(path.read_text(encoding="utf-8"))
    anc = anchor_local(rec)
    rec.setdefault("provenance",{}).setdefault("transparency_anchor", anc)
    path.write_text(json.dumps(rec, indent=2), encoding="utf-8")
    print(f"Anchored locally (index={anc.get('log_index')} root={anc.get('root')[:12]}...)")

if __name__ == "__main__":
    main()
