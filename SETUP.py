"""
SETUP.md — Secure Django E-Commerce Backend

=============================================================
PROJECT STRUCTURE
=============================================================

ecommerce_backend/
├── manage.py
├── requirements.txt
├── .env.example
├── nexmart/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── apps/
    ├── __init__.py
    ├── users/
    │   ├── __init__.py
    │   ├── apps.py
    │   ├── models.py
    │   ├── serializers.py
    │   ├── views.py
    │   ├── urls.py
    │   └── permissions.py
    ├── products/
    │   ├── __init__.py
    │   ├── apps.py
    │   ├── models.py
    │   ├── serializers.py
    │   ├── views.py
    │   ├── urls.py
    │   └── filters.py
    └── orders/
        ├── __init__.py
        ├── apps.py
        ├── models.py
        ├── serializers.py
        ├── views.py
        └── urls.py

=============================================================
QUICK START
=============================================================

1. Create virtual environment and install dependencies:

    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

2. Create the PostgreSQL database:

    psql -U postgres
    CREATE DATABASE nexmart_db;
    CREATE USER nexmart_user WITH PASSWORD 'your-password';
    GRANT ALL PRIVILEGES ON DATABASE nexmart_db TO nexmart_user;
    \q

3. Configure environment:

    cp .env.example .env
    # Edit .env — set SECRET_KEY, DB_PASSWORD, JWT_SIGNING_KEY at minimum.

4. Create __init__.py files:

    touch nexmart/__init__.py
    touch apps/__init__.py
    touch apps/users/__init__.py
    touch apps/products/__init__.py
    touch apps/orders/__init__.py

5. Run migrations:

    python manage.py makemigrations users products orders
    python manage.py migrate

6. Create an admin user:

    python manage.py shell -c "
    from apps.users.models import User
    User.objects.create_superuser(
        email='admin@example.com',
        password='Admin@123!',
        first_name='Admin',
        last_name='User',
    )
    print('Admin created.')
    "

7. Start the development server:

    python manage.py runserver

=============================================================
COMPLETE API REFERENCE
=============================================================

AUTH (prefix: /api/v1/auth/)
------------------------------------------------------------
POST   register/              Create account → returns tokens
POST   login/                 Get JWT pair (5 req/min rate limit)
POST   logout/                Blacklist refresh token
POST   token/refresh/         Rotate access token
GET    profile/               Own profile
PUT    profile/               Full profile update
PATCH  profile/               Partial profile update
POST   change-password/       Change own password
GET    users/                 [Admin] List all users
GET    users/<uuid>/          [Admin] User detail
PATCH  users/<uuid>/          [Admin] Update role/is_active
DELETE users/<uuid>/          [Admin] Soft-ban (is_active=False)

PRODUCTS (prefix: /api/v1/products/)
------------------------------------------------------------
GET    ""                     List active products (search/filter/sort)
GET    featured/              Featured products (home page)
GET    <id>/                  Product detail
GET    categories/            List all categories
GET    categories/<id>/       Category detail
POST   categories/            [Admin] Create category
PUT    categories/<id>/       [Admin] Update category
DELETE categories/<id>/       [Admin] Delete category
GET    admin/                 [Admin] All products (incl. inactive)
POST   admin/                 [Admin] Create product
GET    admin/<id>/            [Admin] Product detail
PUT    admin/<id>/            [Admin] Full update
PATCH  admin/<id>/            [Admin] Partial update
DELETE admin/<id>/            [Admin] Soft-delete (is_active=False)

ORDERS (prefix: /api/v1/orders/)
------------------------------------------------------------
POST   checkout/              Place an order (atomic)
GET    ""                     Own order history
GET    <id>/                  Own order detail
GET    admin/stats/           [Admin] Dashboard statistics
GET    admin/                 [Admin] All orders
GET    admin/<id>/            [Admin] Any order detail
PATCH  admin/<id>/            [Admin] Update status/payment_status

=============================================================
QUERY PARAMETERS — PRODUCTS
=============================================================

GET /api/v1/products/?search=headphone&category=electronics&min_price=50&max_price=500&in_stock=true&is_featured=true&ordering=-price&page=2

search          full-text across name, description, category name
category        category slug (e.g. electronics)
min_price       price >= value
max_price       price <= value
in_stock        true = stock > 0; false = out of stock
is_featured     true = featured only
ordering        price | -price | name | -name | created_at | -created_at
page            page number (PAGE_SIZE = 20)

=============================================================
CHECKOUT REQUEST BODY
=============================================================

POST /api/v1/orders/checkout/
Authorization: Bearer <access_token>
Content-Type:  application/json

{
    "items": [
        {"product_id": 1, "quantity": 2},
        {"product_id": 5, "quantity": 1}
    ],
    "shipping_name":    "Jane Doe",
    "shipping_email":   "jane@example.com",
    "shipping_address": "123 Main Street",
    "shipping_city":    "Nairobi",
    "shipping_country": "Kenya",
    "shipping_postal":  "00100",
    "shipping_phone":   "+254700000000",
    "notes":            "Leave at the door.",
    "payment_method":   "mpesa",
    "payment_reference":"SIM-1234567890"
}

=============================================================
SECURITY SUMMARY
=============================================================

bcrypt hashing        Settings: PASSWORD_HASHERS — BCryptSHA256 first
JWT tokens            SimpleJWT; access 30 min, refresh 7 days
Token rotation        ROTATE_REFRESH_TOKENS=True + BLACKLIST_AFTER_ROTATION
Login rate limit      5 requests/minute via ScopedRateThrottle
Input sanitization    bleach.clean() on all free-text fields
XSS prevention        bleach strips tags; only safe subset allowed in descriptions
SQL injection         Django ORM parameterized queries (no raw SQL anywhere)
Soft delete           Products and users set is_active=False instead of DELETE
Atomic checkout       @transaction.atomic — no partial orders or stock ghosts
Race-safe stock       filter().update() SQL UPDATE (no read-modify-write)
HTTPS enforcement     SECURE_SSL_REDIRECT=True when DEBUG=False
Secure headers        HSTS, X-Frame-Options: DENY, SECURE_CONTENT_TYPE_NOSNIFF
UUID user PKs         Prevents account enumeration attacks
RBAC                  IsAdminRole / IsOwnerOrAdminRole custom DRF permissions
"""
