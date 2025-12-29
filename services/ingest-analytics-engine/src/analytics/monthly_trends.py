"""
Calculate monthly revenue trends.
Shows total sales for each month.
"""

from typing import List, Dict, Any
from ingestion.loader import get_mongo_client
from utils.config import DATABASE_NAME, COLLECTION_NAME
from utils.logger import get_logger

logger = get_logger(__name__)


def get_monthly_revenue() -> List[Dict[str, Any]]:
    """
    Get total revenue for each month.
    
    Returns:
        List of dictionaries with:
        - year: The year
        - month: The month (1-12)
        - revenue: Total sales for that month
    """
    client = get_mongo_client()
    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]
    
    try:
        # Get total sales grouped by year and month
        pipeline = [
            {"$match": {"Order Date": {"$ne": None}}},
            {"$group": {
                "_id": {
                    "year": {"$year": "$Order Date"},
                    "month": {"$month": "$Order Date"}
                },
                "revenue": {"$sum": "$Sales"}
            }},
            {"$sort": {"_id.year": 1, "_id.month": 1}}  # Sort by year, then month
        ]
        
        results = list(collection.aggregate(pipeline))
        
        # Format results nicely
        monthly_data = []
        for result in results:
            monthly_data.append({
                "year": result["_id"]["year"],
                "month": result["_id"]["month"],
                "revenue": result["revenue"]
            })
        
        return monthly_data
    
    finally:
        client.close()
