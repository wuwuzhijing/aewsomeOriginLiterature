#!/usr/bin/env python3
import json, time, re
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
AUTHORS = ROOT / "authors"
DOCS = ROOT / "docs"
INDEX = ROOT / "index.json"

def slugify(s: str) -> str:
    """生成适合文件名的 slug"""
    return re.sub(r"\W+", "-", s.strip())

# 读取所有作者 YAML
authors = []
for f in AUTHORS.rglob("*.yaml"):
    data = yaml.safe_load(f.read_text(encoding="utf-8"))
    authors.append(data)

# 输出 index.json（给程序用）
INDEX.write_text(
    json.dumps({"authors": authors, "generated_at": int(time.time())},
               ensure_ascii=False, indent=2),
    encoding="utf-8"
)

# docs 目录
(DOCS / "authors").mkdir(parents=True, exist_ok=True)

# 首页 index.md
with open(DOCS / "index.md", "w", encoding="utf-8") as f:
    f.write("# Literature Archive\n\n")
    f.write(f"共 {len(authors)} 位作者。\n\n")
    for a in sorted(authors, key=lambda x: x["name"]):
        f.write(f"- [{a['name']}](authors/{slugify(a['name'])}.md)\n")

# Authors 索引页面 authors/index.md
with open(DOCS / "authors" / "index.md", "w", encoding="utf-8") as f:
    f.write("# Authors\n\n")
    for a in sorted(authors, key=lambda x: x["name"]):
        f.write(f"- [{a['name']}](./{slugify(a['name'])}.md)\n")

# 作者页面
for a in authors:
    lines = []
    lines.append(f"# {a['name']}")
    if a.get("tags"):
        lines.append(f"**Tags:** {', '.join(a['tags'])}")
    lines.append("")  # 空行

    # 分组 works
    originals = [w for w in a.get("works", []) if w.get("type") == "original"]
    secondary = [w for w in a.get("works", []) if w.get("type") == "secondary"]

    def render_block(title, works):
        if not works:
            return
        lines.append(f"## {title}")
        for w in works:
            year = w.get("year", "")
            title = w.get("title", "Untitled")
            link = w.get("link", "")
            note = w.get("note", "")
            # 标题加粗
            lines.append(f"- **({year}) {title}**  ")
            lines.append(f"  🔗 [{link}]({link})")
            if note:
                lines.append(f"  > {note}")
            lines.append("")  # 每个条目之间空行

    render_block("原始文献", originals)
    render_block("二手文献", secondary)

    content = "\n".join(lines)
    # 彻底清理字符串里的 '\n' 残留
    content = content.replace("\\n", "\n")

    (DOCS / "authors" / f"{slugify(a['name'])}.md").write_text(
        content, encoding="utf-8"
    )

print(f"Built docs for {len(authors)} authors.")
