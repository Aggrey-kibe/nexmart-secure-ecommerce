# nexmart-secure-ecommerce
Production-ready secure full-stack e-commerce platform built with Django, PostgreSQL, and vanilla JavaScript. Features JWT authentication, role-based access control, rate limiting, and modern responsive UI.


# 🛒 NEXMART — Secure Full-Stack E-Commerce Platform

## Overview

NEXMART is a production-ready full-stack e-commerce platform designed with a strong focus on **security, scalability, and modern UI/UX**.
It demonstrates real-world backend architecture, secure authentication, and responsive frontend design.

---

## 🚀 Features

### Core

* User registration & login
* JWT-based authentication
* Product catalog & filtering
* Shopping cart system
* Checkout (payment simulation)
* Order history
* Admin dashboard (full product & order management)

### 🔐 Security

* Bcrypt password hashing
* JWT authentication (access + refresh tokens)
* Role-Based Access Control (Admin/User)
* Rate limiting on authentication endpoints
* Input validation & sanitization
* Protection against:

  * SQL Injection
  * Cross-Site Scripting (XSS)
  * Cross-Site Request Forgery (CSRF)
* Secure HTTP headers (CSP, HSTS, etc.)
* Environment variable management

---

## 🧠 Tech Stack

### Backend

* Python (Django)
* Django REST Framework
* PostgreSQL

### Frontend

* HTML5
* CSS3 (modern responsive design + animations)
* Vanilla JavaScript (modular architecture)

---

## 📂 Project Structure

/backend → Django backend (API + business logic)
/frontend → UI (HTML, CSS, JS)

---

## ⚙️ Installation

### 1. Clone repository

```bash
git clone https://github.com/YOUR_USERNAME/nexmart-secure-ecommerce.git
cd nexmart-secure-ecommerce
```

### 2. Backend setup

```bash
cd backend
python -m venv venv
source venv/bin/activate   # or venv\Scripts\activate (Windows)
pip install -r requirements.txt
```

### 3. Configure environment

Create `.env` file:

```
SECRET_KEY=your_secret_key
DEBUG=False
DATABASE_URL=postgresql://user:password@localhost:5432/nexmart
JWT_SECRET=your_jwt_secret
```

### 4. Run migrations

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 5. Start server

```bash
python manage.py runserver
```

---

## 🔥 Key Highlights

* Designed with **real-world security practices**
* Clean and scalable backend architecture
* Modular frontend structure (no frameworks)
* Production-ready setup (PostgreSQL + environment configs)

---

## 📸 Demo (Optional)

Add screenshots here after running project.

---

## 📞 Contact

* GitHub: https://github.com/Aggrey-kibe
* LinkedIn: https://linkedin.com/in/aggrey-kibe-1a7a223a0
* Email: [aggreykwamboka62@protonmail.com](mailto:aggreykwamboka62@protonmail.com)

---

## 📄 License

MIT License
