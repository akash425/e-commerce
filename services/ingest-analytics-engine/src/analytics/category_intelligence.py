"""
Calculate average sales by category and sub-category.
Shows which categories perform best.
"""

from typing import List, Dict, Any
from ingestion.loader import get_mongo_client
from utils.config import DATABASE_NAME, COLLECTION_NAME
from utils.logger import get_logger

logger = get_logger(__name__)


def get_category_subcategory_avg_sales() -> List[Dict[str, Any]]:
    """
    Get average sales for each category and sub-category combination.
    
    Returns:
        List of dictionaries with:
        - category: Category name
        - subcategory: Sub-category name
        - avg_sales: Average sales for this combination
    """
    client = get_mongo_client()
    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]
    
    try:
        # Get average sales grouped by category and sub-category
        pipeline = [
            {"$group": {
                "_id": {
                    "category": "$Category",
                    "subcategory": "$Sub-Category"
                },
                "avg_sales": {"$avg": "$Sales"}
            }},
            {"$sort": {"_id.category": 1}}  # Sort by category name
        ]
        
        results = list(collection.aggregate(pipeline))
        
        # Format results nicely
        category_data = []
        for result in results:
            category_data.append({
                "category": result["_id"]["category"],
                "subcategory": result["_id"]["subcategory"],
                "avg_sales": result["avg_sales"]
            })
        
        return category_data
    
    finally:
        client.close()
