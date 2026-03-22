"""
products/serializers.py

Serializers for the product catalog.

Read path (public, no auth):
    CategorySerializer          — category list / detail
    ProductListSerializer       — lightweight card data for listing pages
    ProductDetailSerializer     — full detail including stock and relations

Write path (admin only):
    ProductWriteSerializer      — create / update with full validation
    CategoryWriteSerializer     — create / update a category

Security:
    - bleach.clean() is applied to all free-text fields on write.
    - image_url is checked to start with 'https://' to prevent mixed-content
      and open-redirect via crafted URLs.
    - price must be > 0; stock must be >= 0; discount must be 0–100.
    - Safe HTML tags are allowed in product descriptions (p, br, strong, em,
      ul, li, ol) so admins can use basic formatting; all other tags stripped.
"""

import bleach
from rest_framework import serializers

from .models import Category, Product


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------

_DESCRIPTION_ALLOWED_TAGS = ["p", "br", "strong", "em", "ul", "li", "ol"]


def _sanitize(value: str) -> str:
    """Strip all HTML from a plain-text field."""
    if not value:
        return value
    return bleach.clean(str(value), tags=[], strip=True).strip()


def _sanitize_description(value: str) -> str:
    """
    Allow a safe subset of HTML tags in the product description field.
    All other tags and attributes are stripped.
    """
    if not value:
        return value
    return bleach.clean(
        str(value),
        tags=_DESCRIPTION_ALLOWED_TAGS,
        attributes={},      # no attributes allowed on any tag
        strip=True,
    ).strip()


# ---------------------------------------------------------------------------
# Category serializers
# ---------------------------------------------------------------------------

class CategorySerializer(serializers.ModelSerializer):
    """
    Read-only serializer for category list and nested product display.
    """

    class Meta:
        model  = Category
        fields = ["id", "name", "slug", "description"]
        read_only_fields = fields


class CategoryWriteSerializer(serializers.ModelSerializer):
    """
    Admin write serializer for creating / updating categories.
    Sanitizes name and description before saving.
    """

    class Meta:
        model  = Category
        fields = ["id", "name", "slug", "description"]
        read_only_fields = ["id"]
        extra_kwargs = {"slug": {"required": False}}

    def validate_name(self, value: str) -> str:
        value = _sanitize(value)
        if len(value) < 2:
            raise serializers.ValidationError(
                "Category name must be at least 2 characters."
            )
        return value

    def validate_description(self, value: str) -> str:
        return _sanitize(value)


# ---------------------------------------------------------------------------
# Product — read serializers
# ---------------------------------------------------------------------------

class ProductListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for product listing / card views.

    Returns only the fields needed to render a product card:
        id, name, slug, short_description, price, discount_percent,
        discounted_price, category_name, display_image, is_in_stock,
        is_featured.

    Keeps the payload small — full description and timestamps omitted.
    """

    # Computed properties exposed as read-only fields
    discounted_price = serializers.DecimalField(
        source="discounted_price",
        read_only=True,
        max_digits=10,
        decimal_places=2,
    )
    is_in_stock   = serializers.BooleanField(read_only=True)
    display_image = serializers.CharField(read_only=True)

    # Flatten the category to a single name string (avoids nested object overhead)
    category_name = serializers.CharField(
        source="category.name",
        read_only=True,
        default=None,
    )
    category_slug = serializers.CharField(
        source="category.slug",
        read_only=True,
        default=None,
    )

    class Meta:
        model  = Product
        fields = [
            "id",
            "name",
            "slug",
            "short_description",
            "price",
            "discount_percent",
            "discounted_price",
            "category_name",
            "category_slug",
            "display_image",
            "is_in_stock",
            "is_featured",
        ]


class ProductDetailSerializer(serializers.ModelSerializer):
    """
    Full product detail serializer for the detail endpoint and admin views.

    Includes:
        - Nested category object (id + name + slug)
        - All pricing fields
        - stock count (exact)
        - is_active flag
        - timestamps
    """

    discounted_price = serializers.DecimalField(
        source="discounted_price",
        read_only=True,
        max_digits=10,
        decimal_places=2,
    )
    is_in_stock   = serializers.BooleanField(read_only=True)
    display_image = serializers.CharField(read_only=True)
    category      = CategorySerializer(read_only=True)

    class Meta:
        model  = Product
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "short_description",
            "price",
            "discount_percent",
            "discounted_price",
            "category",
            "display_image",
            "stock",
            "is_in_stock",
            "is_active",
            "is_featured",
            "created_at",
            "updated_at",
        ]


# ---------------------------------------------------------------------------
# Product — write serializer (admin only)
# ---------------------------------------------------------------------------

class ProductWriteSerializer(serializers.ModelSerializer):
    """
    Admin-only serializer for creating and updating products.

    Validation rules:
        name             — required, min 2 chars, HTML stripped
        description      — required, safe HTML subset allowed
        short_description— optional, HTML stripped
        price            — required, must be > 0
        discount_percent — 0–100 inclusive
        stock            — must be >= 0
        image_url        — when provided, must start with 'https://'
        category         — writable FK (pass category id)

    Returns a ProductDetailSerializer representation after save so the
    response body always contains the computed properties (discounted_price,
    display_image, etc.).
    """

    class Meta:
        model  = Product
        fields = [
            "id",
            "name",
            "description",
            "short_description",
            "price",
            "discount_percent",
            "stock",
            "category",
            "image",
            "image_url",
            "is_active",
            "is_featured",
        ]
        read_only_fields = ["id"]
        extra_kwargs = {
            "image":    {"required": False},
            "category": {"required": False, "allow_null": True},
        }

    # ------------------------------------------------------------------
    # Field-level validators
    # ------------------------------------------------------------------

    def validate_name(self, value: str) -> str:
        value = _sanitize(value)
        if len(value) < 2:
            raise serializers.ValidationError(
                "Product name must be at least 2 characters."
            )
        return value

    def validate_description(self, value: str) -> str:
        return _sanitize_description(value)

    def validate_short_description(self, value: str) -> str:
        return _sanitize(value)

    def validate_price(self, value) -> object:
        """Price must be a positive number."""
        if value <= 0:
            raise serializers.ValidationError(
                "Price must be greater than zero."
            )
        return value

    def validate_stock(self, value: int) -> int:
        if value < 0:
            raise serializers.ValidationError(
                "Stock cannot be negative."
            )
        return value

    def validate_discount_percent(self, value: int) -> int:
        if not (0 <= value <= 100):
            raise serializers.ValidationError(
                "Discount must be between 0 and 100."
            )
        return value

    def validate_image_url(self, value: str) -> str:
        """
        Reject non-HTTPS image URLs.
        Motivation: serving mixed HTTP/HTTPS content triggers browser warnings;
        also prevents open-redirect abuse via crafted javascript: URLs.
        """
        if value and not value.startswith("https://"):
            raise serializers.ValidationError(
                "Image URL must use HTTPS."
            )
        return _sanitize(value)

    # ------------------------------------------------------------------
    # Representation — use the detail serializer for responses
    # ------------------------------------------------------------------

    def to_representation(self, instance: Product) -> dict:
        """
        After create/update, return the full ProductDetailSerializer
        representation so API consumers get computed fields immediately.
        """
        return ProductDetailSerializer(instance, context=self.context).data
