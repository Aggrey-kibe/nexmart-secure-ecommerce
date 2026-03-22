"""
products/urls.py

URL patterns for the product catalog.

Mounted under /api/v1/products/ in the root urls.py:
    path("api/v1/products/", include("apps.products.urls"))

Complete URL map:

  Public (no auth):
    GET  /api/v1/products/                      — list active products
    GET  /api/v1/products/featured/             — featured products (home page)
    GET  /api/v1/products/<int:pk>/             — product detail
    GET  /api/v1/products/categories/           — list all categories
    GET  /api/v1/products/categories/<int:pk>/  — category detail

  Admin only:
    POST   /api/v1/products/admin/              — create product
    GET    /api/v1/products/admin/              — list all products (incl. inactive)
    GET    /api/v1/products/admin/<int:pk>/     — admin product detail
    PUT    /api/v1/products/admin/<int:pk>/     — full update
    PATCH  /api/v1/products/admin/<int:pk>/     — partial update
    DELETE /api/v1/products/admin/<int:pk>/     — soft-delete

  Admin only (category write):
    POST   /api/v1/products/categories/         — create category
    PUT    /api/v1/products/categories/<int:pk>/— update category
    PATCH  /api/v1/products/categories/<int:pk>/— partial update category
    DELETE /api/v1/products/categories/<int:pk>/— delete category
"""

from django.urls import path

from .views import (
    AdminProductDetailView,
    AdminProductListCreateView,
    CategoryDetailView,
    CategoryListView,
    FeaturedProductsView,
    ProductDetailView,
    ProductListView,
)

urlpatterns = [
    # ------------------------------------------------------------------
    # Public — product endpoints
    # Note: 'featured/' must come before '<int:pk>/' to prevent Django
    # from trying to cast the string "featured" to an integer.
    # ------------------------------------------------------------------
    path(
        "",
        ProductListView.as_view(),
        name="product-list",
    ),
    path(
        "featured/",
        FeaturedProductsView.as_view(),
        name="product-featured",
    ),
    path(
        "<int:pk>/",
        ProductDetailView.as_view(),
        name="product-detail",
    ),

    # ------------------------------------------------------------------
    # Public GET / Admin write — category endpoints
    # ------------------------------------------------------------------
    path(
        "categories/",
        CategoryListView.as_view(),
        name="category-list",
    ),
    path(
        "categories/<int:pk>/",
        CategoryDetailView.as_view(),
        name="category-detail",
    ),

    # ------------------------------------------------------------------
    # Admin only — product management
    # ------------------------------------------------------------------
    path(
        "admin/",
        AdminProductListCreateView.as_view(),
        name="admin-product-list",
    ),
    path(
        "admin/<int:pk>/",
        AdminProductDetailView.as_view(),
        name="admin-product-detail",
    ),
]
