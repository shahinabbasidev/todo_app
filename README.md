# Todo App

A clean, lightweight **Todo List web application** built with Python.

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

<p align="center">
  <img src="https://placehold.co/800x400/2d3748/ffffff/png?text=Todo+App+Screenshot&font=roboto" alt="Todo App Screenshot" width="800"/>
  <!-- Replace with real screenshot later -->
</p>

## ✨ Features

- Add, edit, complete, and delete tasks
- Mark tasks as completed (with strikethrough & visual feedback)
- Persistent storage (most likely SQLite or file-based)
- Simple and responsive user interface
- Clean & minimal design

## 🛠️ Tech Stack

- **Backend**: Python 3
- **Web framework**: FastAPI
- **Storage**: SQLite / JSON file (please specify)

## 🚀 Demo

(If you deploy it somewhere – Railway, Render, Fly.io, Vercel, etc.)

🔗 **Live Demo**: [https://your-todo-app-url.fly.dev](https://your-todo-app-url.fly.dev)  
(coming soon / add link when deployed)

## 📸 Screenshots

(Add 2–4 real screenshots here later)

<p align="center">
  <img src="docs/screenshots/light-mode.png" width="45%" alt="Light mode"/>
  <img src="docs/screenshots/dark-mode.png" width="45%" alt="Dark mode"/>
</p>

## 🏁 Quick Start

### Prerequisites

- Python 3.9 or higher
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/shahinabbasidev/todo_app.git
cd todo_app

# Create & activate virtual environment (recommended)
python -m venv venv
source venv/bin/activate    # Linux / macOS
venv\Scripts\activate       # Windows

# Install dependencies
pip install -r requirements.txt


# Method 1 – if using uvicorn + ASGI (FastAPI / modern frameworks)
uvicorn core.main:app --reload

# Method 2 – if using Flask / Bottle style
python core/main.py
# or
python app.py
