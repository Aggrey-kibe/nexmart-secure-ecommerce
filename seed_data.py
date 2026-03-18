"""
NEXMART — Database Seed Script
Run via: python manage.py shell < seed_data.py

Creates sample categories and products for demo/development.
Uses Unsplash source URLs for placeholder images (free to use).
"""

import os
import django

# Setup Django (only needed if running standalone)
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nexmart.settings')
# django.setup()

from apps.products.models import Category, Product

print("🌱 Seeding NEXMART database...")

# ── Clear existing seed data ──────────────────────────────────
Product.objects.all().delete()
Category.objects.all().delete()
print("  ✓ Cleared existing data")

# ── Create Categories ─────────────────────────────────────────
categories = {
    'electronics': Category.objects.create(
        name='Electronics',
        description='Cutting-edge gadgets and tech accessories'
    ),
    'clothing': Category.objects.create(
        name='Clothing',
        description='Modern apparel for every occasion'
    ),
    'home': Category.objects.create(
        name='Home & Living',
        description='Furniture, décor, and everything in between'
    ),
    'sports': Category.objects.create(
        name='Sports & Fitness',
        description='Gear up for your active lifestyle'
    ),
    'books': Category.objects.create(
        name='Books',
        description='Expand your mind with our curated library'
    ),
}
print(f"  ✓ Created {len(categories)} categories")

# ── Create Products ───────────────────────────────────────────
products_data = [
    # ── Electronics ──────────────────────────────────────────
    {
        'name': 'Wireless Noise-Cancelling Headphones',
        'category': categories['electronics'],
        'short_description': 'Premium sound with 30-hour battery life',
        'description': '''Experience music the way artists intended. These premium wireless headphones 
feature industry-leading noise cancellation technology that blocks out the world so you can focus on what matters most. 
With 30 hours of battery life, Bluetooth 5.0 connectivity, and cushioned ear cups designed for all-day comfort, 
these headphones redefine what premium audio means. Built-in microphone for hands-free calls. Foldable design for easy travel.''',
        'price': 299.99,
        'discount_percent': 15,
        'stock': 45,
        'image_url': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=600&q=80',
        'is_featured': True,
        'is_active': True,
    },
    {
        'name': 'Smart Watch Pro Series 5',
        'category': categories['electronics'],
        'short_description': 'Health tracking, GPS, and 7-day battery',
        'description': '''The Smart Watch Pro Series 5 is your ultimate fitness companion and daily driver. 
Track your heart rate, sleep quality, blood oxygen levels, and over 100 workout modes automatically. 
Built-in GPS means you leave your phone behind on runs. The 1.4" AMOLED display is always-on and readable in sunlight. 
Water-resistant to 50 meters. Compatible with both iOS and Android.''',
        'price': 449.00,
        'discount_percent': 10,
        'stock': 32,
        'image_url': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=600&q=80',
        'is_featured': True,
        'is_active': True,
    },
    {
        'name': 'Mechanical Gaming Keyboard',
        'category': categories['electronics'],
        'short_description': 'RGB backlit, tactile switches, aluminum frame',
        'description': '''Built for competitive gaming and professional typing alike. The aluminum CNC-machined frame 
provides a premium feel and durability that plastic keyboards simply cannot match. 
Features Cherry MX Blue tactile switches with satisfying click feedback, full per-key RGB lighting with 
16.8 million color options, and N-key rollover for zero missed keystrokes. USB-C detachable cable included.''',
        'price': 159.99,
        'discount_percent': 0,
        'stock': 28,
        'image_url': 'https://images.unsplash.com/photo-1541140532154-b024d705b90a?w=600&q=80',
        'is_featured': False,
        'is_active': True,
    },
    {
        'name': '4K Webcam with Ring Light',
        'category': categories['electronics'],
        'short_description': 'Crystal-clear video for streaming and remote work',
        'description': '''Upgrade your video calls, streams, and content creation with this 4K ultra-high-definition webcam. 
Features a built-in AI-powered autofocus system, dual stereo microphones with noise reduction, and an integrated 
adjustable ring light for perfect lighting in any environment. Plug-and-play USB-C compatibility with Windows, Mac, and Linux. 
Privacy cover included.''',
        'price': 89.99,
        'discount_percent': 20,
        'stock': 60,
        'image_url': 'https://images.unsplash.com/photo-1587202372775-e229f172b9d7?w=600&q=80',
        'is_featured': False,
        'is_active': True,
    },
    {
        'name': 'Portable Bluetooth Speaker',
        'category': categories['electronics'],
        'short_description': '360° sound, waterproof, 24-hour battery',
        'description': '''Take the party anywhere with this rugged, waterproof Bluetooth speaker. 
IPX7 waterproof rating means it can be submerged in up to 1 meter of water for 30 minutes. 
360-degree sound from dual drivers and passive radiator fills any space with rich, full audio. 
Pair two speakers together for true stereo sound. USB-C charging reaches 80% in just 1.5 hours.''',
        'price': 79.99,
        'discount_percent': 5,
        'stock': 75,
        'image_url': 'https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=600&q=80',
        'is_featured': True,
        'is_active': True,
    },

    # ── Clothing ──────────────────────────────────────────────
    {
        'name': 'Merino Wool Premium Hoodie',
        'category': categories['clothing'],
        'short_description': 'Luxuriously soft, temperature-regulating',
        'description': '''Crafted from 100% ethically-sourced merino wool, this hoodie is the last one you'll ever need. 
Merino wool naturally regulates your body temperature, keeping you warm in cold weather and cool when it's warm. 
It's also naturally odor-resistant, meaning you can wear it multiple times before washing. 
The relaxed fit and ribbed cuffs make it perfect for everything from gym sessions to casual evenings out. 
Available in S, M, L, XL, XXL.''',
        'price': 129.00,
        'discount_percent': 0,
        'stock': 120,
        'image_url': 'https://images.unsplash.com/photo-1556821840-3a63f15732ce?w=600&q=80',
        'is_featured': True,
        'is_active': True,
    },
    {
        'name': 'Slim Fit Chino Trousers',
        'category': categories['clothing'],
        'short_description': 'Versatile, stretch comfort fabric',
        'description': '''The perfect pair of trousers that transitions seamlessly from office to evening. 
Made from a premium cotton-elastane blend that stretches with your body while maintaining its shape throughout the day. 
The tailored slim fit is flattering without being restrictive. Machine washable and wrinkle-resistant. 
Features two front slash pockets, two rear welt pockets, and a zip-fly closure.''',
        'price': 69.99,
        'discount_percent': 25,
        'stock': 85,
        'image_url': 'https://images.unsplash.com/photo-1624378439575-d8705ad7ae80?w=600&q=80',
        'is_featured': False,
        'is_active': True,
    },
    {
        'name': 'Classic White Oxford Shirt',
        'category': categories['clothing'],
        'short_description': 'Egyptian cotton, tailored fit, timeless',
        'description': '''Some classics never go out of style. This Oxford shirt is crafted from 100% Egyptian cotton 
with a thread count that makes it softer with every wash. The tailored fit is neither too slim nor too relaxed — 
it simply looks right. Features a button-down collar, chest pocket, and single-button cuffs. 
Dress it up with a blazer or wear it open over a tee. Available in sizes S through XXL.''',
        'price': 85.00,
        'discount_percent': 0,
        'stock': 95,
        'image_url': 'https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=600&q=80',
        'is_featured': False,
        'is_active': True,
    },

    # ── Home & Living ─────────────────────────────────────────
    {
        'name': 'Minimalist Desk Lamp with Wireless Charging',
        'category': categories['home'],
        'short_description': 'Touch-control, 3 color temperatures, Qi charging',
        'description': '''Illuminate your workspace in style with this architect-designed desk lamp. 
Features three color temperature modes (warm white, natural white, cool white) and five brightness levels — 
all controlled with a simple touch on the base. The integrated Qi wireless charging pad keeps your phone 
topped up without cable clutter. Flexible gooseneck allows precise light positioning. 
USB-A pass-through port for additional device charging.''',
        'price': 65.00,
        'discount_percent': 10,
        'stock': 40,
        'image_url': 'https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=600&q=80',
        'is_featured': True,
        'is_active': True,
    },
    {
        'name': 'Handcrafted Ceramic Pour-Over Coffee Set',
        'category': categories['home'],
        'short_description': 'Artisan ceramic dripper + 500ml carafe',
        'description': '''Elevate your morning ritual with this beautifully handcrafted ceramic pour-over set. 
Each piece is individually thrown on a potter's wheel and glazed with a food-safe, lead-free glaze in a 
signature matte finish. The conical dripper promotes even extraction for a balanced, nuanced cup. 
Includes the ceramic dripper, a 500ml glass carafe with cork handle, and a stainless steel measuring spoon. 
Dishwasher safe.''',
        'price': 49.99,
        'discount_percent': 0,
        'stock': 55,
        'image_url': 'https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=600&q=80',
        'is_featured': False,
        'is_active': True,
    },
    {
        'name': 'Scented Soy Candle — Cedarwood & Amber',
        'category': categories['home'],
        'short_description': '60-hour burn time, hand-poured, gift-ready',
        'description': '''Set the mood with this hand-poured soy wax candle. Unlike paraffin candles, 
soy wax burns cleaner and longer, releasing our carefully crafted scent blend of warm cedarwood, 
smoky amber, and a hint of black pepper. The 300g candle provides approximately 60 hours of burn time. 
Packaged in a reusable glass jar with a minimal label — beautiful as a gift or as a treat for yourself. 
Vegan and cruelty-free.''',
        'price': 34.99,
        'discount_percent': 0,
        'stock': 200,
        'image_url': 'https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=600&q=80',
        'is_featured': False,
        'is_active': True,
    },

    # ── Sports & Fitness ──────────────────────────────────────
    {
        'name': 'Adjustable Dumbbell Set (5-50 lbs)',
        'category': categories['sports'],
        'short_description': 'Replaces 15 sets, quick-change mechanism',
        'description': '''Transform your home gym with these innovative adjustable dumbbells. 
A single dial adjustment changes the weight from 5 to 50 pounds in 5-pound increments — 
replacing 15 separate pairs of dumbbells in a footprint smaller than a yoga mat. 
The ergonomic handle with anti-slip grip ensures comfort through every rep. 
Includes a storage tray to keep your space organized. Perfect for beginners and seasoned athletes alike.''',
        'price': 349.00,
        'discount_percent': 15,
        'stock': 18,
        'image_url': 'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=600&q=80',
        'is_featured': True,
        'is_active': True,
    },
    {
        'name': 'Premium Yoga Mat — 6mm Non-Slip',
        'category': categories['sports'],
        'short_description': 'Eco-friendly TPE, alignment lines, carry strap',
        'description': '''Take your practice to the next level with this professional-grade yoga mat. 
Made from eco-friendly TPE (thermoplastic elastomer) — free from PVC, latex, and harmful plasticizers. 
The 6mm thickness provides perfect cushioning for joints without sacrificing stability. 
Laser-etched alignment lines help correct your posture. The double-layer non-slip texture grips both 
the floor and your hands/feet even in a sweaty hot yoga class. Includes a free carry strap.''',
        'price': 55.00,
        'discount_percent': 0,
        'stock': 110,
        'image_url': 'https://images.unsplash.com/photo-1601925228008-d81838a9e1a7?w=600&q=80',
        'is_featured': False,
        'is_active': True,
    },

    # ── Books ─────────────────────────────────────────────────
    {
        'name': 'Clean Code — Robert C. Martin',
        'category': categories['books'],
        'short_description': 'The essential handbook of agile software craftsmanship',
        'description': '''Every developer needs to read Clean Code at least once. Robert C. Martin (Uncle Bob) 
distills decades of experience into actionable principles for writing code that other humans can understand, 
maintain, and extend. Learn how to name things well, write functions that do one thing perfectly, 
handle errors gracefully, and structure your codebase for long-term health. 
Includes real-world code examples and refactoring case studies.''',
        'price': 39.99,
        'discount_percent': 5,
        'stock': 150,
        'image_url': 'https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=600&q=80',
        'is_featured': False,
        'is_active': True,
    },
    {
        'name': 'The Psychology of Money — Morgan Housel',
        'category': categories['books'],
        'short_description': 'Timeless lessons on wealth, greed, and happiness',
        'description': '''Money is more about behavior than it is about spreadsheets. Morgan Housel's 
The Psychology of Money explores 19 short stories about the strange ways people think about money — 
and teaches you how to make better sense of one of life's most important topics. 
Through engaging storytelling and rigorous research, Housel shows that financial success is less about 
intelligence and more about behavior. A must-read for investors, entrepreneurs, and anyone who earns a living.''',
        'price': 24.99,
        'discount_percent': 0,
        'stock': 200,
        'image_url': 'https://images.unsplash.com/photo-1589829085413-56de8ae18c73?w=600&q=80',
        'is_featured': True,
        'is_active': True,
    },

    # One inactive product to demonstrate soft-delete
    {
        'name': 'Discontinued Test Product',
        'category': categories['electronics'],
        'short_description': 'This product has been deactivated',
        'description': 'This product is inactive and will not appear in the shop.',
        'price': 9.99,
        'discount_percent': 0,
        'stock': 0,
        'image_url': '',
        'is_featured': False,
        'is_active': False,  # Soft-deleted — not visible to customers
    },
]

created = 0
for data in products_data:
    Product.objects.create(**data)
    created += 1

print(f"  ✓ Created {created} products ({created - 1} active, 1 inactive)")
print()
print("✅ Seed complete! You can now:")
print("   • Open the shop at http://localhost:5500/shop.html")
print("   • Log in as admin at admin@nexmart.com / Admin@123!")
print("   • Manage products at http://localhost:5500/admin-dashboard.html")
