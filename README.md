# 🎵 Music Streaming App (Flask-Based Web Application)

## 📌 Project Overview

This project is a **full-stack Music Streaming Web Application** built using **Flask** for the backend and **JavaScript-based components** for the frontend. The application supports **user authentication, music management, playlists, admin controls, background tasks, and analytics**, making it a complete end-to-end streaming platform prototype.

The project follows a **modular Flask architecture** with database integration, asynchronous task handling using **Celery**, and REST-style resource management.

---

## 🧱 Tech Stack

### Backend

* **Python (Flask)**
* **Flask-SQLAlchemy**
* **Flask-Login**
* **Flask-RESTful**
* **Celery (Background Tasks)**
* **SQLite (breath_it.sqlite3)**

### Frontend

* **JavaScript (Component-based structure)**
* **Client-side routing**
* **Charts & analytics (static visualizations)**

### Others

* **Email service integration**
* **Role-based access control**
* **Async task worker**

---

## 📁 Project Structure

```
Music-streaming-App-main/
│
├── MUSIC STREAMING APP V2/
│   ├── main.py                 # Application entry point
│   ├── config.py               # App configuration
│   ├── celeryconfig.py         # Celery configuration
│   ├── initial_data.py         # Database seed data
│   ├── requirements.txt        # Python dependencies
│
│   ├── application/
│   │   ├── __init__.py         # App factory
│   │   ├── instances.py        # Flask extensions initialization
│   │   ├── models.py           # Database models
│   │   ├── views.py            # Web routes
│   │   ├── resources.py        # API resources
│   │   ├── sec.py              # Authentication & security logic
│   │   ├── mail_service.py     # Email handling
│   │   ├── tasks.py            # Background Celery tasks
│   │   └── worker.py           # Celery worker
│
│   ├── instance/
│   │   └── breath_it.sqlite3   # SQLite database
│
│   ├── static/
│   │   ├── index.js            # Frontend entry
│   │   ├── router.js           # Client-side routing
│   │   ├── components/         # UI Components
│   │   └── charts/             # Analytics images
│
│   ├── Project Documentation.pdf
│   └── Project Documentation.docx
```

---

## 🚀 Features

### 👤 User Features

* User registration & login
* Browse and stream music
* Playlist creation and management
* Personalized music experience

### 🛠️ Admin Features

* Admin dashboard
* User management
* Song upload & moderation
* Platform analytics

### ⚙️ System Features

* Role-based authentication
* REST APIs for data access
* Background task processing using Celery
* Email notifications
* SQLite database persistence
* Modular and scalable architecture

---

## 🔐 Authentication & Security

* Session-based login system
* Flask-Login integration
* Secure access control using decorators
* Separated security logic (`sec.py`)

---

## 🧵 Asynchronous Tasks

* Background jobs handled using **Celery**
* Dedicated worker (`worker.py`)
* Email sending and long-running tasks executed asynchronously

---

## 📊 Analytics & Visualization

* Static charts generated and stored under `/static/charts`
* Admin insights into user activity and content performance

---

## 🛠️ Installation & Setup

### 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/Music-streaming-App.git
cd "MUSIC STREAMING APP V2"
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run the Application

```bash
python main.py
```

### 5️⃣ (Optional) Start Celery Worker

```bash
celery -A application.worker worker --loglevel=info
```

---

## 📄 Documentation

Detailed project explanation is available in:

* `Project Documentation.pdf`
* `Project Documentation.docx`

---

## 🎯 Use Case

This project is ideal for:

* Academic submissions
* Flask architecture reference
* Full-stack development learning
* Background task implementation demo
* Role-based web applications

---

## 🧠 Learning Highlights

* Clean Flask project structuring
* REST API development
* Secure authentication workflows
* Celery task queues
* Frontend-backend integration

---
