"""
products/views.py

All views for the product catalog.

Public endpoints (no authentication required):
    GET  /products/                  — paginated, filtered, searchable list
    GET  /products/<id>/             — full product detail by PK
    GET  /products/featured/         — up to 8 featured active products
    GET  /products/categories/       — all categories (for sidebar filters)
    GET  /products/categories/<id>/  — single category detail

Admin-only endpoints (role == 'admin' required):
    GET    /products/admin/          — all products including inactive
    POST   /products/admin/          — create a new product
    GET    /products/admin/<id>/     — full detail of any product
    PUT    /products/admin/<id>/     — full update
    PATCH  /products/admin/<id>/     — partial update
    DELETE /products/admin/<id>/     — soft-delete (set is_active=False)

    POST   /products/categories/     — create category (admin only)
    PUT    /products/categories/<id>/— update category (admin only)
    DELETE /products/categories/<id>/— delete category (admin only)

Permissions summary:
    Public list/detail   → AllowAny
    Admin CRUD           → IsAuthenticated + IsAdminRole
    Category write       → IsAuthenticated + IsAdminRole
"""

import logging

from rest_framework import filters, generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from apps.users.permissions import IsAdminRole
from .filters import ProductFilter
from .models import Category, Product
from .serializers import (
    CategorySerializer,
    CategoryWriteSerializer,
    ProductDetailSerializer,
    ProductListSerializer,
    ProductWriteSerializer,
)

logger = logging.getLogger("apps.products")


# ---------------------------------------------------------------------------
# Public — Product listing
# ---------------------------------------------------------------------------

class ProductListView(generics.ListAPIView):
    """
    GET /api/v1/products/

    Return a paginated list of all active products.

    Query parameters (all optional):
        search=<str>         — full-text search across name, description,
                               category name  (DRF SearchFilter)
        ordering=<field>     — e.g. price, -price, name, -created_at
        category=<slug>      — filter by category slug
        min_price=<decimal>  — price >= value
        max_price=<decimal>  — price <= value
        in_stock=true|false  — availability filter
        is_featured=true     — only featured products
        page=<int>           — pagination

    Response:
        {
            "count":    <int>,
            "next":     <url | null>,
            "previous": <url | null>,
            "results":  [<ProductListSerializer>, ...]
        }
    """

    serializer_class   = ProductListSerializer
    permission_classes = [AllowAny]
    filter_backends    = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = ProductFilter
    search_fields   = ["name", "description", "category__name"]
    ordering_fields = ["price", "created_at", "name"]
    ordering        = ["-created_at"]   # default ordering

    def get_queryset(self):
        """
        Return only is_active=True products with category pre-fetched
        to avoid N+1 queries on category_name / category_slug fields.
        """
        return (
            Product.objects
            .filter(is_active=True)
            .select_related("category")
        )


class ProductDetailView(generics.RetrieveAPIView):
    """
    GET /api/v1/products/<id>/

    Return full detail for a single active product.
    Returns 404 for inactive products (as if they don't exist).
    """

    serializer_class   = ProductDetailSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return (
            Product.objects
            .filter(is_active=True)
            .select_related("category")
        )


class FeaturedProductsView(generics.ListAPIView):
    """
    GET /api/v1/products/featured/

    Return up to 8 featured, active products for the home page.
    No pagination — the count is bounded by the queryset slice.
    """

    serializer_class   = ProductListSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return (
            Product.objects
            .filter(is_active=True, is_featured=True)
            .select_related("category")
            .order_by("-created_at")[:8]
        )


# ---------------------------------------------------------------------------
# Public — Category listing
# ---------------------------------------------------------------------------

class CategoryListView(generics.ListCreateAPIView):
    """
    GET  /api/v1/products/categories/   — list all categories (public)
    POST /api/v1/products/categories/   — create a category (admin only)
    """

    queryset = Category.objects.all().order_by("name")

    def get_serializer_class(self):
        if self.request.method == "GET":
            return CategorySerializer
        return CategoryWriteSerializer

    def get_permissions(self):
        """
        Dynamic permissions:
            GET  → AllowAny       (category list used in public filter sidebar)
            POST → IsAdminRole    (only admins can create categories)
        """
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated(), IsAdminRole()]


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/v1/products/categories/<id>/   — category detail (public)
    PUT    /api/v1/products/categories/<id>/   — update (admin only)
    PATCH  /api/v1/products/categories/<id>/   — partial update (admin only)
    DELETE /api/v1/products/categories/<id>/   — delete (admin only)
    """

    queryset = Category.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return CategorySerializer
        return CategoryWriteSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated(), IsAdminRole()]


# ---------------------------------------------------------------------------
# Admin — Product management
# ---------------------------------------------------------------------------

class AdminProductListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/v1/products/admin/
        Return ALL products (including is_active=False) for admin management.
        Supports ?search and ?is_active=true|false filtering.

    POST /api/v1/products/admin/
        Create a new product.
        Request body uses ProductWriteSerializer.
        Response body returns ProductDetailSerializer (via to_representation).
    """

    permission_classes = [IsAuthenticated, IsAdminRole]
    filter_backends    = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields      = ["name", "category__name"]
    ordering_fields    = ["price", "created_at", "stock", "name"]
    ordering           = ["-created_at"]

    def get_queryset(self):
        """
        Include all products regardless of is_active.
        Optionally filter by ?is_active=true or ?is_active=false.
        """
        qs = Product.objects.all().select_related("category")

        is_active_param = self.request.query_params.get("is_active")
        if is_active_param is not None:
            if is_active_param.lower() == "true":
                qs = qs.filter(is_active=True)
            elif is_active_param.lower() == "false":
                qs = qs.filter(is_active=False)

        return qs

    def get_serializer_class(self):
        """
        GET  → ProductDetailSerializer (shows all fields including is_active)
        POST → ProductWriteSerializer  (validates input; returns detail shape)
        """
        if self.request.method == "GET":
            return ProductDetailSerializer
        return ProductWriteSerializer

    def perform_create(self, serializer):
        product = serializer.save()
        logger.info(
            "Product created | id=%s | name=%s | by=%s",
            product.id,
            product.name,
            self.request.user.email,
        )


class AdminProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/v1/products/admin/<id>/   — full detail of any product
    PUT    /api/v1/products/admin/<id>/   — full update
    PATCH  /api/v1/products/admin/<id>/   — partial update (any subset of fields)
    DELETE /api/v1/products/admin/<id>/   — soft-delete: sets is_active=False

    Soft-delete rationale:
        Products are referenced by OrderItem rows. Hard-deleting them would
        either violate FK constraints (with PROTECT) or erase order history
        (with CASCADE).  Setting is_active=False hides the product from all
        public endpoints while preserving relational integrity.
    """

    permission_classes = [IsAuthenticated, IsAdminRole]
    queryset           = Product.objects.all().select_related("category")

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ProductDetailSerializer
        return ProductWriteSerializer

    def update(self, request, *args, **kwargs):
        """
        Force partial=True on all PATCH requests.
        PUT requests still require all non-read-only fields.
        """
        if request.method == "PATCH":
            kwargs["partial"] = True
        return super().update(request, *args, **kwargs)

    def perform_update(self, serializer):
        product = serializer.save()
        logger.info(
            "Product updated | id=%s | name=%s | by=%s",
            product.id,
            product.name,
            self.request.user.email,
        )

    def destroy(self, request, *args, **kwargs):
        """
        Override DELETE to perform a soft-delete instead of a hard delete.

        Sets is_active=False and returns 200 with a confirmation message
        (rather than 204 No Content) so the client can confirm which product
        was affected.
        """
        product = self.get_object()
        product.is_active = False
        product.save(update_fields=["is_active"])

        logger.warning(
            "Product soft-deleted | id=%s | name=%s | by=%s",
            product.id,
            product.name,
            request.user.email,
        )
        return Response(
            {
                "message": f'Product "{product.name}" has been deactivated.',
                "id":      product.id,
            },
            status=status.HTTP_200_OK,
        )
