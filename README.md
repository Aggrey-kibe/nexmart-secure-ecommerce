# ⬡ NEXMART — Secure Full-Stack E-Commerce Platform

> **Production-ready** Django + Vanilla JS e-commerce application with enterprise-grade security.  
> Built as a professional portfolio project demonstrating full-stack architecture, RESTful APIs, and real security implementation.

---

##  Table of Contents

1. [Tech Stack](#tech-stack)
2. [Security Features](#security-features)
3. [Quick Start](#quick-start)
4. [Project Structure](#project-structure)
5. [API Reference](#api-reference)
6. [Deployment Guide](#deployment-guide)
7. [Environment Variables](#environment-variables)

---

##  Tech Stack

| Layer      | Technology                                      |
|------------|-------------------------------------------------|
| Backend    | Python 3.11+, Django 4.2, Django REST Framework |
| Auth       | JWT (SimpleJWT), bcrypt password hashing        |
| Database   | PostgreSQL 15+                                  |
| Frontend   | HTML5, CSS3, Vanilla JavaScript (ES6+)          |
| Security   | CSRF, XSS, rate limiting, secure headers        |
| Production | Gunicorn, WhiteNoise (static files)             |

---

##  Security Features

| Feature               | Implementation                                        |
|-----------------------|-------------------------------------------------------|
| Password Hashing      | BCryptSHA256 (via Django PASSWORD_HASHERS)             |
| Authentication        | JWT access + refresh tokens (SimpleJWT)               |
| Token Refresh         | Automatic refresh with rotation + blacklisting        |
| Rate Limiting         | 5 login attempts/minute (DRF ScopedRateThrottle)      |
| SQL Injection         | Django ORM parameterized queries (no raw SQL)         |
| XSS Prevention        | Input sanitization (bleach), CSP headers, JS escaping |
| CSRF Protection       | Django CSRF middleware (API uses JWT instead)         |
| Secure Headers        | CSP, HSTS, X-Frame-Options, Permissions-Policy        |
| Role-Based Access     | CUSTOMER vs ADMIN roles with custom DRF permissions   |
| Soft Delete           | Products deactivated, never hard-deleted              |
| Atomic Transactions   | Checkout uses `@transaction.atomic` for consistency   |
| Request Logging       | Security events logged with IP and timestamp          |

---

##  Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL 15+
- Git

### 1. Clone and navigate
```bash
git clone https://github.com/yourusername/nexmart.git
cd nexmart/backend
```

### 2. Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate          # Linux/Mac
# venv\Scripts\activate           # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment
```bash
cp .env.example .env
nano .env                         # Fill in your actual values
```

### 5. Create PostgreSQL database
```sql
-- Run in psql:
CREATE DATABASE nexmart_db;
CREATE USER nexmart_user WITH PASSWORD 'your-password';
GRANT ALL PRIVILEGES ON DATABASE nexmart_db TO nexmart_user;
```

### 6. Run migrations
```bash
# Create __init__.py files first
mkdir -p logs
touch apps/__init__.py apps/users/__init__.py apps/products/__init__.py
touch apps/orders/__init__.py middleware/__init__.py nexmart/__init__.py

python manage.py makemigrations
python manage.py migrate
```

### 7. Create admin user
```bash
python manage.py createsuperuser --email admin@nexmart.com
```

Or programmatically:
```bash
python manage.py shell -c "
from apps.users.models import User
User.objects.create_superuser(
    email='admin@nexmart.com',
    password='Admin@123!',
    first_name='Admin',
    last_name='User',
)
print('Admin created')
"
```

### 8. Seed sample data
```bash
python manage.py shell < seed_data.py
```

### 9. Start backend
```bash
python manage.py runserver
# API available at: http://localhost:8000/api/v1/
```

### 10. Serve frontend
```bash
cd ../frontend
python -m http.server 5500
# Open: http://localhost:5500
```

---

##  Project Structure

```
nexmart/
├── backend/
│   ├── nexmart/           # Django project config
│   │   ├── settings.py    # Full security config
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── apps/
│   │   ├── users/         # Auth, registration, profiles
│   │   ├── products/      # Catalog, categories
│   │   └── orders/        # Cart → Checkout → Orders
│   ├── middleware/
│   │   └── security.py    # Custom security headers
│   ├── seed_data.py       # Sample data
│   ├── requirements.txt
│   └── .env.example
└── frontend/
    ├── index.html         # Home page
    ├── shop.html          # Product listing
    ├── product.html       # Product detail
    ├── cart.html          # Shopping cart
    ├── checkout.html      # Checkout flow
    ├── auth.html          # Login / Register
    ├── orders.html        # Order history
    ├── admin-dashboard.html
    ├── css/
    │   ├── main.css       # Design system
    │   └── pages/pages.css
    └── js/
        ├── core/          # api.js, auth.js, store.js
        ├── components/    # toast.js, loader.js, navbar.js
        └── pages/         # Per-page scripts
```

---

##  API Reference

### Authentication
| Method | Endpoint                    | Auth | Description                  |
|--------|-----------------------------|------|------------------------------|
| POST   | `/api/v1/auth/login/`       | None | Login, returns JWT tokens    |
| POST   | `/api/v1/auth/register/`    | None | Register new user            |
| POST   | `/api/v1/auth/logout/`      | JWT  | Logout, blacklists refresh   |
| POST   | `/api/v1/auth/token/refresh/`| None | Refresh access token        |
| GET    | `/api/v1/auth/profile/`     | JWT  | Get current user profile     |
| PATCH  | `/api/v1/auth/profile/`     | JWT  | Update profile               |
| POST   | `/api/v1/auth/change-password/`| JWT | Change password            |

### Products
| Method | Endpoint                        | Auth  | Description               |
|--------|---------------------------------|-------|---------------------------|
| GET    | `/api/v1/products/`             | None  | List products (paginated) |
| GET    | `/api/v1/products/<id>/`        | None  | Product detail            |
| GET    | `/api/v1/products/featured/`    | None  | Featured products         |
| GET    | `/api/v1/products/categories/`  | None  | List categories           |
| GET    | `/api/v1/products/admin/`       | Admin | All products (incl. inactive)|
| POST   | `/api/v1/products/admin/`       | Admin | Create product            |
| PATCH  | `/api/v1/products/admin/<id>/`  | Admin | Update product            |
| DELETE | `/api/v1/products/admin/<id>/`  | Admin | Soft-delete product       |

### Orders
| Method | Endpoint                      | Auth  | Description               |
|--------|-------------------------------|-------|---------------------------|
| POST   | `/api/v1/orders/checkout/`    | JWT   | Place an order            |
| GET    | `/api/v1/orders/`             | JWT   | My order history          |
| GET    | `/api/v1/orders/<id>/`        | JWT   | Order detail              |
| GET    | `/api/v1/orders/admin/`       | Admin | All orders                |
| GET    | `/api/v1/orders/admin/stats/` | Admin | Dashboard statistics      |
| PATCH  | `/api/v1/orders/admin/<id>/`  | Admin | Update order status       |

### Query Parameters (Products)
```
/api/v1/products/?search=headphones&category=electronics&min_price=50&max_price=300&in_stock=true&ordering=-price&page=1
```

---

##  Deployment Guide (Ubuntu + Nginx)

### 1. Install system dependencies
```bash
sudo apt update
sudo apt install python3-pip python3-venv postgresql nginx
```

### 2. Configure PostgreSQL
```bash
sudo -u postgres psql
# Then run CREATE DATABASE / CREATE USER commands
```

### 3. Set up application
```bash
cd /var/www/nexmart/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# Edit .env: set DEBUG=False, real SECRET_KEY, DB credentials
python manage.py migrate
python manage.py collectstatic
```

### 4. Gunicorn service (`/etc/systemd/system/nexmart.service`)
```ini
[Unit]
Description=NEXMART Gunicorn
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/nexmart/backend
ExecStart=/var/www/nexmart/backend/venv/bin/gunicorn \
    nexmart.wsgi:application \
    --workers 4 \
    --bind unix:/run/nexmart.sock
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

### 5. Nginx config (`/etc/nginx/sites-available/nexmart`)
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    # Frontend (static files)
    location / {
        root /var/www/nexmart/frontend;
        try_files $uri $uri/ /index.html;
    }

    # Backend API
    location /api/ {
        proxy_pass http://unix:/run/nexmart.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Media files
    location /media/ {
        alias /var/www/nexmart/backend/media/;
    }
}
```

---

##  Default Credentials

| Role     | Email                    | Password     |
|----------|--------------------------|--------------|
| Admin    | aggreykwamboka@protinmail.com        | Brightvibe@2026   |
| Customer | (register via /auth.html)| (your choice)|

>  **Change the admin password immediately after first login!**

---

##  License

MIT License. Built for portfolio demonstration purposes.

---

*Built with ❤️ using Django, DRF, JWT authentication, bcrypt, and Vanilla JS*
