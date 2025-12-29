"""
Flask API service for e-commerce analytics.

Provides endpoints to access analytics data from MongoDB.
"""

import os
import sys
from pathlib import Path

from flask import Flask, jsonify
from flask_cors import CORS

# Try to import dotenv for environment variable loading
try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None  # dotenv not installed, that's okay

# Add ingest-analytics-engine src to path for imports
# Try multiple possible paths (for Docker and local development)
possible_paths = [
    Path(__file__).parent / "ingest-analytics-engine" / "src",  # Docker path
    Path(__file__).parent.parent / "ingest-analytics-engine" / "src",  # Local dev path
]
for path in possible_paths:
    if path.exists():
        sys.path.insert(0, str(path))
        break

# Analytics imports (after path setup)
from analytics.product_intelligence import get_top_products
from analytics.monthly_trends import get_monthly_revenue
from analytics.category_intelligence import get_category_subcategory_avg_sales
from analytics.yearly_growth import get_yearly_growth
from utils.logger import get_logger

# Load environment variables
if load_dotenv:
    project_root = Path(__file__).parent.parent.parent
    env_file = project_root / ".env"
    if env_file.exists():
        load_dotenv(env_file)

logger = get_logger(__name__)

app = Flask(__name__)
CORS(app)


@app.route('/api/analytics/top-products', methods=['GET'])
def top_products():
    """Get top products by sales."""
    try:
        products = get_top_products()
        return jsonify({"data": products, "status": "success"}), 200
    except Exception as e:
        logger.error(f"Error fetching top products: {e}", exc_info=True)
        return jsonify({
            "error": "Failed to fetch top products",
            "message": str(e),
            "status": "error"
        }), 500


@app.route('/api/analytics/monthly-revenue', methods=['GET'])
def monthly_revenue():
    """Get monthly revenue data."""
    try:
        revenue = get_monthly_revenue()
        return jsonify({"data": revenue, "status": "success"}), 200
    except Exception as e:
        logger.error(f"Error fetching monthly revenue: {e}", exc_info=True)
        return jsonify({
            "error": "Failed to fetch monthly revenue",
            "message": str(e),
            "status": "error"
        }), 500


@app.route('/api/analytics/category-avg-sales', methods=['GET'])
def category_avg_sales():
    """Get category and subcategory average sales."""
    try:
        sales = get_category_subcategory_avg_sales()
        return jsonify({"data": sales, "status": "success"}), 200
    except Exception as e:
        logger.error(f"Error fetching category avg sales: {e}", exc_info=True)
        return jsonify({
            "error": "Failed to fetch category average sales",
            "message": str(e),
            "status": "error"
        }), 500


@app.route('/api/analytics/yearly-growth', methods=['GET'])
def yearly_growth():
    """Get yearly growth data."""
    try:
        growth = get_yearly_growth()
        return jsonify({"data": growth, "status": "success"}), 200
    except Exception as e:
        logger.error(f"Error fetching yearly growth: {e}", exc_info=True)
        return jsonify({
            "error": "Failed to fetch yearly growth",
            "message": str(e),
            "status": "error"
        }), 500


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({"status": "healthy"}), 200


if __name__ == '__main__':
    api_host = os.getenv("API_HOST", "0.0.0.0")
    api_port = int(os.getenv("API_PORT", "5000"))
    debug_mode = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    app.run(debug=debug_mode, host=api_host, port=api_port)

