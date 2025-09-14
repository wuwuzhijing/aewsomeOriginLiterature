## 📄 `README_EN.md`


# 📚 Literature Archive

[![GitHub Pages](https://img.shields.io/badge/docs-GitHub%20Pages-blue)](https://<your-username>.github.io/<repo-name>/)
[![Contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](CONTRIBUTING.md)
[![License](https://img.shields.io/github/license/<your-username>/<repo-name>)](LICENSE)

An **open-source, cross-disciplinary literature archive** for:

- 🔎 Collecting **primary sources** (original papers, manuscripts, books)  
- 📖 Linking to **secondary sources** (biographies, commentaries, academic history)  
- 🌐 Publishing a **searchable index website** via [GitHub Pages](https://<your-username>.github.io/<repo-name>/)

👉 **No copyrighted PDFs are stored.** We only keep metadata (title, year, tags, links, notes).

---

## ✨ Features

- **Structured storage**: one YAML file per author  
- **Automated workflow**: validate schema, build index, deploy site with CI  
- **Clear presentation**: author pages separated into *Primary* / *Secondary* sources  
- **Powerful search**: full-text search powered by MkDocs Material  
- **Link health**: planned link checking + Internet Archive fallback  

---

## 📂 Project Structure

```plaintext
.
├── authors/              # Author YAML files
│   ├── A/
│   │   └── einstein.yaml
│   └── H/
│       └── hegel.yaml
├── docs/                 # Auto-generated site (no manual edits)
├── scripts/              # Validation and build scripts
│   ├── build_index.py
│   └── validate.py
├── mkdocs.yml            # MkDocs config
├── requirements.txt      # Python dependencies
└── README.md             # Project description
````

---

## 🚀 Quick Start

### Local preview

```bash
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>

pip install -r requirements.txt

# Validate author files
python scripts/validate.py

# Build index & docs
python scripts/build_index.py

# Serve locally
mkdocs serve
```

Browse 👉 `http://127.0.0.1:8000`

### Online access

Latest site is hosted at **GitHub Pages**:
👉 [https://<your-username>.github.io/<repo-name>/](https://<your-username>.github.io/<repo-name>/)

---

## 🛠 Contributing

We welcome all contributions! ✨

1. **Add a new author or work**

   * Place a new YAML file under `authors/<Initial>/`
   * Follow the schema in [schemas/author.schema.json](schemas/author.schema.json)

2. **Fix or update links**

   * Replace broken links or add Internet Archive snapshots

3. **Improve scripts / site**

   * Enhance `build_index.py`
   * Customize MkDocs config

### Workflow

* Fork this repo
* Create a new branch
* Commit changes
* Open a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

---

## 📜 Data Format Example

`authors/A/einstein.yaml`:

```yaml
name: "Albert Einstein"
tags: ["physics", "relativity"]
works:
  - type: "original"
    title: "Zur Elektrodynamik bewegter Körper"
    year: 1905
    link: "https://einsteinpapers.press.princeton.edu/vol2-doc/154"
    note: "Special relativity original paper"
  - type: "secondary"
    title: "Einstein: His Life and Universe"
    year: 2007
    link: "https://www.goodreads.com/book/show/91164"
    note: "Biography by Walter Isaacson"
```

---

## 🤝 Community

* Questions → [GitHub Issues](../../issues)
* Contributions → [Pull Requests](../../pulls)
* Star ⭐ this repo to support and spread the project

---

## 📄 License

This project is licensed under [MIT License](LICENSE).
All external links are for academic reference only. Copyright remains with original authors and publishers.

