#!/usr/bin/env python3
import json
import yaml
import sys
from pathlib import Path
from jsonschema import validate, ValidationError

ROOT = Path(__file__).resolve().parents[1]
AUTHORS = ROOT / "authors"
SCHEMA_FILE = ROOT / "schemas" / "author.schema.json"

def load_schema():
    with open(SCHEMA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def validate_file(yaml_path, schema):
    try:
        data = yaml.safe_load(yaml_path.read_text(encoding="utf-8"))
        validate(instance=data, schema=schema)
        print(f"✅ {yaml_path} is valid.")
        return True
    except ValidationError as e:
        print(f"❌ {yaml_path} is invalid.")
        print(f"   Error: {e.message}")
        print(f"   Path: {'/'.join([str(p) for p in e.path])}")
        return False
    except Exception as e:
        print(f"⚠️ {yaml_path} could not be validated: {e}")
        return False

def main():
    schema = load_schema()
    yaml_files = list(AUTHORS.rglob("*.yaml"))
    if not yaml_files:
        print("No author YAML files found.")
        sys.exit(1)

    print(f"Found {len(yaml_files)} YAML files to validate.\n")

    all_valid = True
    for f in yaml_files:
        if not validate_file(f, schema):
            all_valid = False

    if not all_valid:
        print("\n❌ Some files are invalid. Please fix them before committing.")
        sys.exit(1)
    else:
        print("\n✅ All YAML files are valid!")

if __name__ == "__main__":
    main()