# 🚀 CodeSprint

> A GitHub Code Snippet Fetch & Filtering Engine built using FastAPI and React (Vite).

CodeSprint is a full-stack application that fetches real-world code files from GitHub repositories, intelligently filters them based on language rules, and serves structured code snippets via a REST API to a React frontend.

It is designed as a foundation for building coding practice platforms, snippet engines, and AI-powered learning systems.

---

## 📌 Tech Stack

### 🖥 Frontend
- React (Vite)
- Axios
- TailwindCSS (optional)

### ⚙ Backend
- FastAPI
- GitHub REST API
- Pydantic
- Uvicorn
- CORS Middleware

---

## ✨ Features

- 🔍 Fetch repository file tree from GitHub
- 📂 Language-based file filtering
- 🚫 Ignore unwanted files (tests, configs, docs, etc.)
- 📄 Fetch raw file content
- 🧠 Basic difficulty-based filtering logic
- 🌐 RESTful API architecture
- ⚡ High-performance asynchronous backend
- 🔄 Proper CORS handling for frontend integration

---

## 🧠 How It Works

1. Backend fetches repository tree from GitHub API.
2. Filters files based on:
   - Allowed language extensions
   - Ignored keywords
   - Ignored filenames
3. Fetches raw file content.
4. Returns structured snippets through API.
5. React frontend consumes and displays snippets.

---

### 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/CodeSprint.git
cd CodeSprint
```

---

## ⚙ Backend Setup (FastAPI)

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate environment

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn app.main:app --reload
```

Backend runs at:

```
http://localhost:8000
```

---

## 🎨 Frontend Setup (React + Vite)

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend runs at:

```
http://localhost:5173
```
