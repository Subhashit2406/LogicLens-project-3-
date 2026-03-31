# 🔍 LogicLens — Codebase Graph Chat

> An intelligent tool that parses Python codebases, maps function relationships into a knowledge graph, and lets you explore your code visually — powered by **Neo4j**, **ChromaDB**, and **Tree-sitter**.

---

## ✨ Features

- 📂 **Codebase Analysis** — Scans any Python project directory and extracts all functions
- 🔗 **Call Graph Generation** — Maps which functions call which, stored as a Neo4j graph
- 👤 **Author Attribution** — Uses Git blame to tag each function with its author
- 🧠 **Semantic Search** — Stores function source code in ChromaDB for vector-based search
- 🌐 **Visual Graph UI** — Interactive web interface to explore the codebase graph

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Web Framework | Flask |
| Graph Database | Neo4j |
| Vector Database | ChromaDB |
| Code Parser | Tree-sitter |
| Git Integration | GitPython |
| Frontend | HTML / JavaScript |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- [Neo4j Desktop](https://neo4j.com/download/) running locally on `bolt://localhost:7687`
- Git

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/Subhashit2406/LogicLens-project-3-.git
cd LogicLens-project-3-

# 2. Create and activate virtual environment
python -m venv .venv

# Windows
.\.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

# 3. Install dependencies
pip install flask neo4j chromadb tree-sitter tree-sitter-python gitpython
```

### Configuration

Open `app.py` and `extractor.py` and update the Neo4j credentials if needed:

```python
URI  = "neo4j://127.0.0.1:7687"
AUTH = ("neo4j", "your_password")
```

### Run the App

```bash
python app.py
```

Then open your browser at: **http://127.0.0.1:5000**

---

## 📁 Project Structure

```
LogicLens-project-3-/
│
├── app.py              # Flask web server & API routes
├── extractor.py        # Core: Tree-sitter parser + Neo4j + ChromaDB writer
├── sample_code.py      # Sample Python file for testing analysis
├── test_chroma.py      # ChromaDB integration tests
│
├── templates/
│   └── index.html      # Frontend UI for graph visualization
│
├── .gitignore
└── README.md
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET`  | `/` | Web UI |
| `POST` | `/api/analyze` | Analyze a project directory |
| `GET`  | `/api/graph` | Fetch graph nodes and edges |

### Example: Analyze a Project

```bash
curl -X POST http://127.0.0.1:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"path": "C:/path/to/your/project"}'
```

---

## 🤝 Contributing (Team Workflow)

We use a **Fork → Branch → Pull Request** model. All changes go through review before merging into `master`.

### Step-by-step for team members:

#### 1. Fork the Repository
Click **Fork** on the top-right of this GitHub page to create your own copy.

#### 2. Clone Your Fork
```bash
git clone https://github.com/YOUR_USERNAME/LogicLens-project-3-.git
cd LogicLens-project-3-
```

#### 3. Create a Feature Branch
```bash
# Always branch off from master
git checkout master
git pull origin master
git checkout -b feature/your-feature-name
```

> 🔖 **Naming convention:** `feature/`, `fix/`, `docs/`  
> Examples: `feature/search-ui`, `fix/neo4j-query`, `docs/update-readme`

#### 4. Make Your Changes & Commit
```bash
git add .
git commit -m "feat: describe what you changed"
```

#### 5. Push Your Branch
```bash
git push origin feature/your-feature-name
```

#### 6. Open a Pull Request
- Go to the original repo: [LogicLens-project-3-](https://github.com/Subhashit2406/LogicLens-project-3-)
- Click **"Compare & Pull Request"**
- Fill in what you changed and why
- Submit for review ✅

> ⚠️ **The `master` branch is protected.** Only the repo owner can merge PRs. Do not push directly to `master`.

---

## 📜 License

This project is for academic/group use. Please contact the repo owner before external distribution.

---

## 👤 Author

**Subhashit** — [@Subhashit2406](https://github.com/Subhashit2406)
