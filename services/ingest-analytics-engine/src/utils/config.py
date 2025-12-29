"""
Simple configuration settings for the project.
All settings are in one place for easy understanding.
"""

import os
from pathlib import Path

# Try to load environment variables from .env file
try:
    from dotenv import load_dotenv
    # Find .env file in project root (3 levels up from this file)
    project_root = Path(__file__).parent.parent.parent.parent.parent
    env_file = project_root / ".env"
    if env_file.exists():
        load_dotenv(env_file)
except ImportError:
    pass  # dotenv not installed, that's okay

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
LOGS_DIR = PROJECT_ROOT / "logs"
CSV_FILE = DATA_DIR / "orders.csv"
CHECKPOINT_FILE = DATA_DIR / "checkpoint.json"

# MongoDB settings
MONGO_URI = os.getenv("MONGO_URI", "")
DATABASE_NAME = "ecommerce"
COLLECTION_NAME = "orders"

# Processing settings
BATCH_SIZE = 1000
MAX_RETRIES = 3
RETRY_DELAY = 1  # seconds

# Date format in CSV files
DATE_FORMAT = "%m/%d/%Y"

# Required fields for order validation
REQUIRED_FIELDS = [
    "Order ID",
    "Order Date",
    "Product ID",
    "Category",
    "Sub-Category",
    "Sales"
]

