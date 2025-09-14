#!/usr/bin/env python3
import json, time, re
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
AUTHORS = ROOT/'authors'
DOCS = ROOT/'docs'
INDEX = ROOT/'index.json'

def slugify(s): return re.sub(r'\W+','-',s)

authors = []
for f in AUTHORS.rglob('*.yaml'):
    data = yaml.safe_load(f.read_text())
    authors.append(data)

DOCS.mkdir(exist_ok=True)
(DOCS/'authors').mkdir(parents=True, exist_ok=True)

INDEX.write_text(json.dumps({"authors":authors,"generated_at":int(time.time())}, ensure_ascii=False, indent=2))

with open(DOCS/'index.md','w',encoding='utf-8') as f:
    f.write('# Literature Archive\n')
    for a in authors:
        f.write(f"- [{a['name']}](authors/{slugify(a['name'])}.md)\n")

for a in authors:
    (DOCS/'authors'/f"{slugify(a['name'])}.md").write_text(f"# {a['name']}\n", encoding='utf-8')
