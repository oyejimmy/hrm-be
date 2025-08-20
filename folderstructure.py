import os

# Define folder structure
folders = [
    "app/auth",
    "app/core",
    "app/database",
    "app/modules",
    "app/api",
    "alembic",
    "tests",
]

files = {
    "app/__init__.py": "",
    "app/main.py": "from fastapi import FastAPI\n\napp = FastAPI()\n\n@app.get('/')\ndef root():\n    return {'message': 'HRM-BE API is running 🚀'}\n",
    "app/auth/__init__.py": "",
    "app/core/__init__.py": "",
    "app/database/__init__.py": "",
    "app/modules/__init__.py": "",
    "app/api/__init__.py": "",
    "requirements.txt": "fastapi\nuvicorn\nsqlalchemy\nalembic\npydantic\npytest\npython-jose[cryptography]\npasslib[bcrypt]\n",
    ".gitignore": "venv/\n__pycache__/\n*.sqlite3\n.env\n",
    "README.md": "# HRM-BE\n\nBackend service built with FastAPI and SQLite.",
}

# Create folders
for folder in folders:
    os.makedirs(folder, exist_ok=True)

# Create files
for file_path, content in files.items():
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

print("✅ HRM-BE project structure created successfully!")
