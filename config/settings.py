import os
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
DB_PATH = PROJECT_ROOT / "ecommerce.db"

# Database configuration
DATABASE_URL = f"sqlite:///{DB_PATH}"

# Data file paths
RAW_DATA_PATH = DATA_DIR / "messy_ecommerce_sales_data.csv"
CLEAN_DATA_PATH = DATA_DIR / "cleaned_ecommerce_sales_data.csv"

# Product categorization mapping
PRODUCT_CATEGORIES = {
    "Home": ["Blender", "Microwave", "Vacuum", "Lamp"],
    "Electronics": ["Smartphone", "Smartwatch", "Headphones", "Laptop"],
    "Sports": ["Tennis Racket", "Basketball", "Yoga Mat", "Football"],
    "Books": ["Science", "Biography", "Comics", "Fiction"],
    "Clothing": ["Shoes", "T-shirt", "Jacket", "shoes", "Jeans"]
}

# Data cleaning configuration
CLEANING_RULES = {
    "price_patterns": {
        "remove_letters": r'[a-zA-Z]+',
        "remove_currency": r'[$]',
        "replace_with": "Null"
    },
    "category_exclusions": [
        'electronic', 'ELECTRONICS', 'electronics', 'sports'
    ]
}