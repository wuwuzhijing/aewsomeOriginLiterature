#!/usr/bin/env python3
import sys, json
from pathlib import Path
import yaml
from jsonschema import validate

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads(Path(ROOT/'schemas/author.schema.json').read_text())
for f in Path(ROOT/'authors').rglob('*.yaml'):
    data = yaml.safe_load(f.read_text())
    validate(instance=data, schema=SCHEMA)
print("All author files valid.")
