import argparse, os, json, uuid, time
from pathlib import Path
from .crypto import rotating_pepper
from .receipts import make_ir, sign_receipt, frontier_score

def _key_bytes():
    key = os.environ.get("IDEA_LAYER_HMAC_KEY","changeme-dev-key").encode("utf-8")
    kid = os.environ.get("IDEA_LAYER_KEY_ID","default")
    return kid, key

def cmd_ir(args):
    kid, key = _key_bytes()
    pep = rotating_pepper(int(time.time()) // 86400)
    idea_id = str(uuid.uuid4())
    ir = make_ir(
        idea_uuid=idea_id,
        creator_anon_id=args.creator,
        idea_text_len=args.len,
        idea_summary_text=args.summary,
        prompt_text=args.prompt,
        kappa=args.kappa,
        delta_hol={"prompt":0,"tool":0,"retrieval":0,"model":0,"cache":0},
        ucr=args.ucr,
        cycles=0, contradictions=0, guard_failures=["none"],
        plausibility_p=args.plaus,
        novelty_bucket=args.novelty,
        license_scope=args.scope,
        consent_version="v1",
        retention_days=365,
        privacy_secret=key, privacy_pepper=pep
    )
    ir = sign_receipt(ir, kid, key)
    Path(args.out).write_text(json.dumps(ir, indent=2), encoding="utf-8")
    print(f"Wrote IR → {args.out}")

def main():
    p = argparse.ArgumentParser(prog="idea-layer", description="Idea Layer v0.1 CLI")
    sub = p.add_subparsers(dest="cmd")

    pir = sub.add_parser("ir", help="Create + sign an Idea Receipt")
    pir.add_argument("--creator", required=True)
    pir.add_argument("--summary", required=True)
    pir.add_argument("--prompt", default="")
    pir.add_argument("--len", type=int, default=280)
    pir.add_argument("--kappa", type=float, default=0.2)
    pir.add_argument("--ucr", type=float, default=0.1)
    pir.add_argument("--plaus", type=float, default=0.6)
    pir.add_argument("--novelty", choices=["low","medium","high"], default="medium")
    pir.add_argument("--scope", choices=["audit-only","research-noncommercial","train-critic","limited-production","full-production"], default="research-noncommercial")
    pir.add_argument("--out", default="ir.sample.json")
    pir.set_defaults(func=cmd_ir)

    args = p.parse_args()
    if not args.cmd:
        p.print_help(); return
    args.func(args)
