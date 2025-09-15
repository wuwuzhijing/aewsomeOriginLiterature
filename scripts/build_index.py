#!/usr/bin/env python3
import json, time, re, shutil
from pathlib import Path
import yaml
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
AUTHORS = ROOT / "authors"
DOCS = ROOT / "docs"
INDEX = ROOT / "index.json"

# 改成你的仓库地址
GITHUB_BASE = "https://github.com/wuwuzhijing/awesomeOriginLiterature/blob/main"

def slugify(s: str) -> str:
    """生成适合文件名的 slug"""
    return re.sub(r"\W+", "-", s.strip())

# 读取作者 YAML，并按 slug 去重
raw_entries = []
for f in sorted(AUTHORS.rglob("*.yaml")):
    try:
        data = yaml.safe_load(f.read_text(encoding="utf-8"))
        if not isinstance(data, dict) or "name" not in data:
            print(f"⚠️ 跳过 {f}（缺少 name 字段或格式异常）")
            continue
        raw_entries.append({"file": f, "data": data})
    except Exception as e:
        print(f"❌ 解析失败 {f}: {e}")

by_slug = {}
duplicates = []
for entry in raw_entries:
    name = entry["data"]["name"]
    slug = slugify(name)
    if slug in by_slug:
        duplicates.append((name, by_slug[slug]["file"], entry["file"]))
    else:
        by_slug[slug] = entry

if duplicates:
    print("\n⚠️ 发现作者重名（将只保留第一份，同名的其余忽略）：")
    for name, first_f, dup_f in duplicates:
        print(f"   - {name}: {first_f}（保留） | {dup_f}（忽略）")
    print("")

# 去重后的作者与文件
author_files = [v["file"] for v in by_slug.values()]
authors = [v["data"] for v in by_slug.values()]

# 输出 index.json
INDEX.write_text(
    json.dumps({"authors": authors, "generated_at": int(time.time())},
               ensure_ascii=False, indent=2),
    encoding="utf-8"
)

# docs 目录
(DOCS / "authors").mkdir(parents=True, exist_ok=True)

# 首页
with open(DOCS / "index.md", "w", encoding="utf-8") as f:
    f.write("# Literature Archive\n\n")
    f.write(f"共 {len(authors)} 位作者。\n\n")
    for a in sorted(authors, key=lambda x: x["name"]):
        f.write(f"- [{a['name']}](authors/{slugify(a['name'])}.md)\n")

# Authors 索引页
with open(DOCS / "authors" / "index.md", "w", encoding="utf-8") as f:
    f.write("# Authors\n\n")
    for a in sorted(authors, key=lambda x: x["name"]):
        f.write(f"- [{a['name']}](./{slugify(a['name'])}.md)\n")

# 逐个作者生成页面
for f, a in zip(author_files, authors):
    lines = []
    slug = slugify(a["name"])

    # 标题 & GitHub 入口
    lines.append(f"# {a['name']}")
    rel_path = f.relative_to(ROOT).as_posix()
    github_url = f"{GITHUB_BASE}/{rel_path}"
    lines.append(f"[🔗 在 GitHub 上查看/编辑该作者文件]({github_url})\n")

    # 标签
    if a.get("tags"):
        lines.append(f"**Tags:** {', '.join(a['tags'])}\n")

    # 年表：通配搜索 *_timeline.md 并复制到 docs/authors/
    matches = list(AUTHORS.rglob(f"{slug}_timeline.md"))
    if matches:
        timeline_src = matches[0]
        timeline_dst = DOCS / "authors" / f"{slug}_timeline.md"
        shutil.copyfile(timeline_src, timeline_dst)
        lines.append(f"[📜 {a['name']} 年表]({slug}_timeline.md)\n")

    # 文献渲染
    originals = [w for w in a.get("works", []) if w.get("type") == "original"]
    secondary = [w for w in a.get("works", []) if w.get("type") == "secondary"]

    def render_block(title, works):
        if not works:
            return
        lines.append(f"## {title}")
        for idx, w in enumerate(works, 1):
            year = w.get("year", "")
            note = w.get("note", "")
            wt = w.get("title", {})

            if isinstance(wt, dict):
                original = wt.get("original", "Untitled")
                en = wt.get("en")
                zh = wt.get("zh")
            else:
                original = str(wt)
                en = zh = None

            lines.append(f"{idx}. **({year}) {original}**  ")
            if en:
                lines.append(f"   *English:* {en}  ")
            if zh:
                lines.append(f"   *中文:* {zh}  ")

            links = w.get("links", [])
            if isinstance(links, str):
                links = [links]
            for link in links:
                host = (urlparse(link).hostname or "Link").replace("www.", "")
                lines.append(f"   🔗 [{host}]({link})  ")

            if note:
                lines.append(f"   > {note}")
            lines.append("")

    render_block("Original Literature", originals)
    render_block("Secondary Literature", secondary)

    # 资源渲染
    resources = a.get("resources", [])
    if resources:
        lines.append("## Resources")
        for idx, r in enumerate(resources, 1):
            title = r.get("title", "Untitled")
            note = r.get("note", "")
            links = r.get("links", [])
            if isinstance(links, str):
                links = [links]

            lines.append(f"{idx}. {title}")
            for link in links:
                host = (urlparse(link).hostname or "Link").replace("www.", "")
                lines.append(f"   🔗 [{host}]({link})  ")
            if note:
                lines.append(f"   > {note}")
            lines.append("")

    content = "\n".join(lines).replace("\\n", "\n")
    (DOCS / "authors" / f"{slug}.md").write_text(content, encoding="utf-8")

print(f"Built docs for {len(authors)} authors.")