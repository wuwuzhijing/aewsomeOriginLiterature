#!/usr/bin/env python3
import json, time, re
from pathlib import Path
import yaml
from urllib.parse import urlparse

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

    timeline_path = (AUTHORS / slugify(a['name'])[0].upper() /
                 f"{slugify(a['name'])}_timeline.md")
    print(f"Timeline check for {a['name']}: {timeline_path}")
    if timeline_path.exists():
        target_path = DOCS / "authors" / f"{slugify(a['name'])}_timeline.md"
        print(f"Timeline check for {a['name']}: {target_path}")
        # 复制内容到 docs
        target_path.write_text(timeline_path.read_text(encoding="utf-8"), encoding="utf-8")

        # 在作者页面加一个跳转链接
        lines.append(f"[📜 {a['name']} 年表]({slugify(a['name'])}_timeline.md)")
        lines.append("")
        
    # 分组 works
    originals = [w for w in a.get("works", []) if w.get("type") == "original"]
    secondary = [w for w in a.get("works", []) if w.get("type") == "secondary"]

    def render_block(title, works):
        if not works:
            return
        lines.append(f"## {title}")
        for idx, w in enumerate(works, 1):
            year = w.get("year", "")
            links = w.get("links", [])
            note = w.get("note", "")
            title = w.get("title", {})
            
            if isinstance(title, dict):
                original = title.get("original", "Untitled")
                en = title.get("en")
                zh = title.get("zh")
            else:
                original = str(title)
                en = zh = None
            lines.append(f"{idx}. **({year}) {original}**  ")
            #lines.append(f"- **({year}) {original}**  ")

            # 翻译分行显示
            if en:
                lines.append(f"  *English:* {en}  ")
            if zh:
                lines.append(f"  *中文:* {zh}  ")

            # 链接
            if isinstance(links, str):  # 兼容旧数据
                links = [links]

            for link in links:
                hostname = urlparse(link).hostname or "Link"
                hostname = hostname.replace("www.", "")
                lines.append(f"  🔗 [{hostname}]({link})  ")
            # 备注说明
            if note:
                lines.append(f"  > {note}")

            lines.append("")  # 条目之间空行

    render_block("Original  Literature", originals)
    render_block("Secondary Literature", secondary)
    
    resources = a.get("resources", [])

    def render_resources(resources):
        if not resources:
            return
        lines.append("## 其他资源")
        for idx, r in enumerate(resources, 1):
            title = r.get("title", "Untitled")
            note = r.get("note", "")

            links = r.get("links", [])
            if isinstance(links, str):
                links = [links]

            # 标题
            lines.append(f"{idx}. {title}")
            # 多个链接逐行展示
            for link in links:
                lines.append(f"   🔗 [{link}]({link})  ")

            if note:
                lines.append(f"   > {note}")
            lines.append("")

    render_resources(resources)

    content = "\n".join(lines)
    # 彻底清理字符串里的 '\n' 残留
    content = content.replace("\\n", "\n")

    (DOCS / "authors" / f"{slugify(a['name'])}.md").write_text(
        content, encoding="utf-8"
    )

print(f"Built docs for {len(authors)} authors.")
