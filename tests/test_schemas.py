import json, pathlib
from jsonschema import validate

root = pathlib.Path(__file__).resolve().parents[1]
schemas = {
    "ir": json.loads((root/"schemas/v0.1/ir.schema.json").read_text(encoding="utf-8")),
    "vr": json.loads((root/"schemas/v0.1/vr.schema.json").read_text(encoding="utf-8")),
    "lr": json.loads((root/"schemas/v0.1/lr.schema.json").read_text(encoding="utf-8"))
}

def _load(p): return json.loads(p.read_text(encoding="utf-8"))

def test_ir_ok():
    data = _load(root/"tests/samples_ok/ir.ok.json")
    validate(instance=data, schema=schemas["ir"])

def test_vr_ok():
    data = _load(root/"tests/samples_ok/vr.ok.json")
    validate(instance=data, schema=schemas["vr"])

def test_lr_ok():
    data = _load(root/"tests/samples_ok/lr.ok.json")
    validate(instance=data, schema=schemas["lr"])
