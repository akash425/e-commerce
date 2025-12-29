"""
Calculate yearly sales growth.
Shows total sales per year and growth percentage compared to previous year.
"""

from typing import List, Dict, Any
from ingestion.loader import get_mongo_client
from utils.config import DATABASE_NAME, COLLECTION_NAME
from utils.logger import get_logger

logger = get_logger(__name__)


def get_yearly_growth() -> List[Dict[str, Any]]:
    """
    Get sales by year and calculate growth percentage.
    
    Returns:
        List of dictionaries with:
        - year: The year
        - total_sales: Total sales for that year
        - growth_percent: Growth compared to previous year (None for first year)
    """
    client = get_mongo_client()
    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]
    
    try:
        # Get total sales grouped by year
        pipeline = [
            {"$match": {"Order Date": {"$ne": None}}},
            {"$group": {
                "_id": {"$year": "$Order Date"},
                "total_sales": {"$sum": "$Sales"}
            }},
            {"$sort": {"_id": 1}}  # Sort by year (oldest first)
        ]
        
        results = list(collection.aggregate(pipeline))
        
        # Calculate growth percentage for each year
        yearly_data = []
        previous_sales = None
        
        for result in results:
            year = result["_id"]
            current_sales = result["total_sales"]
            
            # Calculate growth: (current - previous) / previous * 100
            if previous_sales is None:
                # First year - no previous year to compare
                growth_percent = None
            else:
                growth_percent = ((current_sales - previous_sales) / previous_sales) * 100
            
            yearly_data.append({
                "year": year,
                "total_sales": current_sales,
                "growth_percent": growth_percent
            })
            
            # Remember this year's sales for next iteration
            previous_sales = current_sales
        
        return yearly_data
    
    finally:
        client.close()
