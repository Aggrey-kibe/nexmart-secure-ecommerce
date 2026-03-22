"""
products/filters.py

django-filter FilterSet for the Product model.

Supports these query parameters on GET /api/v1/products/:
    ?category=<slug>          filter by category slug
    ?min_price=<decimal>      price >= value
    ?max_price=<decimal>      price <= value
    ?in_stock=true|false      stock > 0
    ?is_featured=true|false   featured flag
    ?search=<string>          full-text search (handled by DRF SearchFilter,
                              but listed here for documentation completeness)

Example:
    /api/v1/products/?category=electronics&min_price=50&max_price=300&in_stock=true
"""

import django_filters

from .models import Product


class ProductFilter(django_filters.FilterSet):
    """
    FilterSet applied to the public product listing endpoint.

    All filters operate only on is_active=True products because the view's
    base queryset already restricts to active products.
    """

    # Filter by category slug string rather than category PK.
    # This keeps URLs human-readable: ?category=electronics
    category = django_filters.CharFilter(
        field_name="category__slug",
        lookup_expr="iexact",
        label="Category slug",
    )

    # Price range filters
    min_price = django_filters.NumberFilter(
        field_name="price",
        lookup_expr="gte",
        label="Minimum price",
    )
    max_price = django_filters.NumberFilter(
        field_name="price",
        lookup_expr="lte",
        label="Maximum price",
    )

    # Stock availability — ?in_stock=true returns only products with stock > 0
    in_stock = django_filters.BooleanFilter(
        method="filter_in_stock",
        label="In stock only",
    )

    # Featured flag
    is_featured = django_filters.BooleanFilter(
        field_name="is_featured",
        label="Featured products only",
    )

    class Meta:
        model  = Product
        fields = ["category", "min_price", "max_price", "in_stock", "is_featured"]

    @staticmethod
    def filter_in_stock(queryset, name, value):
        """
        When value=True  → return products where stock > 0.
        When value=False → return products where stock == 0 (out-of-stock).
        """
        if value:
            return queryset.filter(stock__gt=0)
        return queryset.filter(stock=0)
