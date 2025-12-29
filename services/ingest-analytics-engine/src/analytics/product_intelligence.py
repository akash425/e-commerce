"""
Find top products by sales.
Shows which products generate the most revenue.
"""

from typing import List, Dict, Any
from ingestion.loader import get_mongo_client
from utils.config import DATABASE_NAME, COLLECTION_NAME
from utils.logger import get_logger

logger = get_logger(__name__)


def get_top_products(limit: int = 5) -> List[Dict[str, Any]]:
    """
    Get the top products by total sales.
    
    Args:
        limit: How many top products to return (default: 5)
    
    Returns:
        List of dictionaries with:
        - product_id: Product ID
        - total_sales: Total sales for this product
    """
    client = get_mongo_client()
    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]
    
    try:
        # Get total sales grouped by product, sorted by sales (highest first)
        pipeline = [
            {"$group": {
                "_id": "$Product ID",
                "total_sales": {"$sum": "$Sales"}
            }},
            {"$sort": {"total_sales": -1}},  # Sort descending (highest first)
            {"$limit": limit}  # Only return top N products
        ]
        
        results = list(collection.aggregate(pipeline))
        
        # Format results nicely
        top_products = []
        for result in results:
            top_products.append({
                "product_id": result["_id"],
                "total_sales": result["total_sales"]
            })
        
        return top_products
    
    finally:
        client.close()
