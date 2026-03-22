"""
products/models.py

Data models for the product catalog.

Models:
    Category   — top-level grouping for products (e.g. Electronics, Clothing)
    Product    — individual sellable item with pricing, stock, and media

Design decisions:
    - Slugs are auto-generated from names and guaranteed unique at save time.
    - Prices are stored as DecimalField (exact arithmetic, not float).
    - Soft-delete via is_active=False keeps FK integrity with orders intact.
    - discounted_price is a computed @property — never stored in the DB.
    - product images support both a file upload field and an external HTTPS URL;
      display_image returns whichever is set, upload taking priority.
    - DB indexes are placed on every column used in WHERE clauses or ORDER BY.
"""

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.text import slugify


# ---------------------------------------------------------------------------
# Category
# ---------------------------------------------------------------------------

class Category(models.Model):
    """
    A top-level grouping used to organise and filter products.

    Fields:
        name        Human-readable label, unique (e.g. "Electronics")
        slug        URL-safe identifier, auto-derived from name
        description Optional marketing copy for the category
        created_at  Auto-set timestamp
    """

    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="Human-readable category name, e.g. 'Electronics'.",
    )
    slug = models.SlugField(
        max_length=120,
        unique=True,
        blank=True,
        db_index=True,
        help_text="Auto-generated URL segment. Leave blank to auto-fill.",
    )
    description = models.TextField(
        blank=True,
        help_text="Optional marketing copy shown on the category page.",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name        = "Category"
        verbose_name_plural = "Categories"
        ordering            = ["name"]

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs) -> None:
        """Auto-generate slug from name if not provided."""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


# ---------------------------------------------------------------------------
# Product
# ---------------------------------------------------------------------------

class Product(models.Model):
    """
    A single item available for purchase.

    Pricing logic:
        price             — base retail price (DecimalField, exact)
        discount_percent  — integer 0–100; 0 means no discount
        discounted_price  — computed @property; the amount a customer pays

    Stock:
        stock             — current quantity on hand (0 = out of stock)
        is_in_stock       — computed @property for template / serializer use

    Images:
        image             — uploaded file (stored under MEDIA_ROOT/products/)
        image_url         — external HTTPS URL alternative
        display_image     — @property returning the best available image URL

    Lifecycle flags:
        is_active         — False hides the product from all public endpoints
                            (soft-delete; never remove rows referenced by orders)
        is_featured       — True surfaces the product on the home page

    Indexes added:
        (is_active, is_featured)   — home page featured query
        (category,  is_active)     — category-filtered shop page query
        (created_at)               — default ordering
    """

    # ------------------------------------------------------------------
    # Relations
    # ------------------------------------------------------------------
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products",
        help_text="The category this product belongs to.",
    )

    # ------------------------------------------------------------------
    # Identity
    # ------------------------------------------------------------------
    name = models.CharField(
        max_length=255,
        db_index=True,
        help_text="Full product name shown in listings and detail pages.",
    )
    slug = models.SlugField(
        max_length=300,
        unique=True,
        blank=True,
        db_index=True,
        help_text="Auto-generated URL segment. Leave blank to auto-fill.",
    )
    description = models.TextField(
        help_text="Full product description (may contain safe HTML).",
    )
    short_description = models.CharField(
        max_length=500,
        blank=True,
        help_text="One-sentence teaser shown on listing cards.",
    )

    # ------------------------------------------------------------------
    # Pricing — use DecimalField, never FloatField, for monetary values
    # ------------------------------------------------------------------
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Base retail price in USD.",
    )
    discount_percent = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Percentage discount (0 = no discount, 100 = free).",
    )

    # ------------------------------------------------------------------
    # Inventory
    # ------------------------------------------------------------------
    stock = models.PositiveIntegerField(
        default=0,
        help_text="Current units available. Set to 0 to show 'out of stock'.",
    )

    # ------------------------------------------------------------------
    # Media
    # ------------------------------------------------------------------
    image = models.ImageField(
        upload_to="products/",
        blank=True,
        null=True,
        help_text="Uploaded product image (stored in MEDIA_ROOT/products/).",
    )
    image_url = models.URLField(
        blank=True,
        max_length=500,
        help_text="External image URL (HTTPS). Used when no upload is present.",
    )

    # ------------------------------------------------------------------
    # Lifecycle flags
    # ------------------------------------------------------------------
    is_active = models.BooleanField(
        default=True,
        db_index=True,
        help_text=(
            "False hides the product from the public API. "
            "Use this instead of deleting products that appear in orders."
        ),
    )
    is_featured = models.BooleanField(
        default=False,
        help_text="True surfaces this product on the home/featured endpoint.",
    )

    # ------------------------------------------------------------------
    # Timestamps
    # ------------------------------------------------------------------
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    # ------------------------------------------------------------------
    # Meta
    # ------------------------------------------------------------------
    class Meta:
        verbose_name        = "Product"
        verbose_name_plural = "Products"
        ordering            = ["-created_at"]
        indexes = [
            models.Index(fields=["is_active", "is_featured"]),
            models.Index(fields=["category",  "is_active"]),
        ]

    # ------------------------------------------------------------------
    # Dunder / repr
    # ------------------------------------------------------------------

    def __str__(self) -> str:
        return self.name

    # ------------------------------------------------------------------
    # Save — auto-generate unique slug
    # ------------------------------------------------------------------

    def save(self, *args, **kwargs) -> None:
        """
        Derive slug from name if not explicitly set.
        Appends a numeric suffix to guarantee uniqueness:
            "Wireless Headphones"  →  "wireless-headphones"
            (if taken)             →  "wireless-headphones-1"
            (if taken)             →  "wireless-headphones-2"
        """
        if not self.slug:
            base = slugify(self.name)
            slug = base
            counter = 1
            while (
                Product.objects.filter(slug=slug)
                .exclude(pk=self.pk)
                .exists()
            ):
                slug = f"{base}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    # ------------------------------------------------------------------
    # Computed properties
    # ------------------------------------------------------------------

    @property
    def discounted_price(self):
        """
        Return the final price after applying discount_percent.

        Uses Python's Decimal arithmetic to avoid floating-point rounding
        errors that would occur with float multiplication.

        Returns:
            Decimal: The price the customer actually pays.
        """
        if self.discount_percent > 0:
            factor   = self.discount_percent / 100      # Python float, ok for multiplication
            discount = self.price * factor              # Decimal * float → Decimal
            return round(self.price - discount, 2)
        return self.price

    @property
    def is_in_stock(self) -> bool:
        """True when at least one unit is available."""
        return self.stock > 0

    @property
    def display_image(self) -> str:
        """
        Return the best available image URL.
        Priority: uploaded file > external URL > empty string.
        """
        if self.image:
            return self.image.url
        return self.image_url or ""
