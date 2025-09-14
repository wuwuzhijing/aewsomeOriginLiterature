<p align="center">
  <img src="logo.svg" alt="Literature Archive Logo" width="120"/>
</p>

# 📚Literature Archive

[![GitHub Pages](https://img.shields.io/badge/docs-GitHub%20Pages-blue)](https://<你的用户名>.github.io/<仓库名>/)
[![Contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](CONTRIBUTING.md)
[![License](https://img.shields.io/github/license/<你的用户名>/<仓库名>)](LICENSE)

一个开源的 **跨学科文献索引与可视化项目**，用于：
- 🔎 持续收集各个领域的 **原始文献**（论文、专著、手稿）
- 📖 关联同一作者的 **二手文献**（传记、评论、学术史研究）
- 🌐 在 [GitHub Pages](https://wuwuzhihing.github.io/awesomeOriginLiterature/) 上生成 **可检索、可浏览的索引网站**

👉 **我们不存放原文 PDF**，只保存元数据（标题、年份、标签、链接、备注），确保版权合规。


## ✨ 功能亮点

- **结构化存储**：每位作者一个 YAML 文件，便于协作与版本控制  
- **自动化构建**：CI 自动校验格式、生成索引与网页  
- **直观展示**：作者页面分为「原始文献」「二手文献」  
- **强大搜索**：基于 MkDocs Material，可按作者、标题、标签快速检索  
- **长期可用**：定期校验文献链接，标记失效并可接入 Internet Archive 快照  


## 📂 项目结构

```bash
.
├── authors/              # 作者文献数据（YAML 格式）
│   ├── A/
│   │   └── einstein.yaml
│   └── H/
│       └── hegel.yaml
├── docs/                 # 自动生成的文档 (无需手工编辑)
├── scripts/              # 构建与校验脚本
│   ├── build_index.py
│   └── validate.py
├── mkdocs.yml            # MkDocs 配置
├── requirements.txt      # Python 依赖
└── README.md             # 项目说明
```
## 🚀 快速开始

### 本地预览

```bash
git clone https://github.com/<你的用户名>/<仓库名>.git
cd <仓库名>

pip install -r requirements.txt

# 校验 YAML 文件格式
python scripts/validate.py

# 构建索引与网页
python scripts/build_index.py

# 启动本地预览
mkdocs serve
```

浏览器访问 👉 `http://127.0.0.1:8000`

### 在线访问

最新网站托管在 **GitHub Pages**：
👉 [https://<你的用户名>.github.io/<仓库名>/](https://wuwuzhijing.github.io/awesomeOriginLiterature/)

- 示例：https://wuwuzhijing.github.io/awesomeOriginLiterature/ 
---

## 🛠 如何贡献

我们非常欢迎社区贡献！✨
你可以通过以下方式参与：

1. **添加新作者或文献**

   * 在 `authors/<首字母>/` 下新建或修改 YAML 文件
   * 格式请参考 [schemas/author.schema.json](schemas/author.schema.json)

2. **修复或更新链接**

   * 如果发现某篇文献的链接失效，可以提交 PR 更新为新链接
   * 或者添加 Internet Archive 的快照链接作为备用

3. **改进脚本与网站**

   * 优化 `build_index.py` 的生成逻辑
   * 改善 MkDocs 配置（UI/搜索/导航）

### 提交流程

* Fork 本仓库
* 在新分支中提交更改
* 发起 Pull Request

请阅读 [CONTRIBUTING.md](CONTRIBUTING.md) 获取详细指南。

---

## 📜 数据格式示例

`authors/A/einstein.yaml`:

```yaml
name: "Albert Einstein"
tags: ["physics", "relativity"]
works:
  - type: "original"
    title: "Zur Elektrodynamik bewegter Körper"
    year: 1905
    link: "https://einsteinpapers.press.princeton.edu/vol2-doc/154"
    note: "狭义相对论原始论文"
  - type: "secondary"
    title: "Einstein: His Life and Universe"
    year: 2007
    link: "https://www.goodreads.com/book/show/91164"
    note: "Walter Isaacson 传记"
```

---

## 🤝 社区与交流

* 提问或讨论 → [GitHub Issues](../../issues)
* 提交修改 → [Pull Requests](../../pulls)
* Star ⭐️ 支持我们，让更多人看到

---

## 📄 License

本项目采用 [MIT License](LICENSE)。
文献链接仅作学术研究索引之用，原始版权归原作者及出版方所有。
