# 🧑‍💼 HRM-BE (Human Resource Management Backend)

## 📌 Overview
This repo hrm-be is a backend service for a Human Resource Management System built with **FastAPI** and **SQLite**.  
It provides RESTful APIs for user authentication, employee management, attendance tracking, leave management, payroll, and more.

The project is designed to be modular, scalable, and easy to extend with additional HRM features.

---

## 🚀 Tech Stack
- **Framework:** [FastAPI](https://fastapi.tiangolo.com/)  
- **Database:** SQLite (default, can be switched to PostgreSQL/MySQL)  
- **ORM:** SQLAlchemy  
- **Migrations:** Alembic  
- **Validation:** Pydantic  
- **Authentication:** JWT-based  

---

## 📂 Project Structure
```
HRM-BE/
├── app/
│   ├── auth/              # Authentication (login, signup, JWT)
│   ├── core/              # Core config and security utilities
│   ├── database/          # Database connection & models
│   ├── modules/           # HRM modules (employee, payroll, leave, etc.)
│   ├── api/               # API routers
│   ├── main.py            # Entry point
│   └── __init__.py
├── alembic/               # Database migrations
├── tests/                 # Unit and integration tests
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
```

---

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/oyejimmy/hrm-be.git
cd hrm-be
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Database Migrations
```bash
alembic upgrade head
```

### 5. Start the FastAPI Server
```bash
uvicorn app.main:app --reload
```

The server will run at:  
👉 [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 📖 API Documentation
FastAPI automatically generates interactive API docs:

- Swagger UI → [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)  
- ReDoc → [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)  

---

## ✅ Features (Implemented)
- [x] User Authentication (Signup, Login, JWT)  
- [x] Employee Profile Management  
- [x] Attendance Tracking  
- [x] Leave Management  
- [x] Payroll System  
- [x] Recruitment Workflow  
- [x] Performance Tracking  
- [x] Training Management  
- [x] Announcements & Events  
- [x] Teams & Projects (Org)  

### Seeded Accounts
- Admin: `admin@example.com` / `admin123`
- Manager: `lead@example.com` / `lead123`
- Employee: `emp@example.com` / `emp123`

### Quickstart
```bash
uvicorn app.main:app --reload
```
Open http://127.0.0.1:8000/docs

---

## 🧪 Running Tests
```bash
pytest
```

---

## 📌 Contributing
1. Fork the repo  
2. Create a feature branch (`git checkout -b feature-name`)  
3. Commit changes (`git commit -m 'Add new feature'`)  
4. Push branch (`git push origin feature-name`)  
5. Create a Pull Request  

---

## 📜 License
This project is licensed under the MIT License.  
See [LICENSE](LICENSE) for more details.
