"""
Transforms order data into the right data types.
Converts dates to datetime objects and numbers to floats.
"""

from datetime import datetime
from typing import Dict, Any
from utils.logger import get_logger
from utils.config import DATE_FORMAT

logger = get_logger(__name__)


def transform_order(row: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert order data to proper types.
    
    Args:
        row: Validated order dictionary
    
    Returns:
        Dictionary with dates as datetime objects and sales as float
    """
    transformed = {}
    order_id = row.get("Order ID", "unknown")
    
    for key, value in row.items():
        # Empty strings become None
        if isinstance(value, str) and not value:
            transformed[key] = None
            continue
        
        # Convert date fields to datetime objects
        if key in ("Order Date", "Ship Date"):
            if value:
                try:
                    transformed[key] = datetime.strptime(value, DATE_FORMAT)
                except (ValueError, TypeError) as e:
                    logger.warning(f"Order {order_id}: Could not parse {key} '{value}' - {e}")
                    transformed[key] = None
            else:
                transformed[key] = None
        
        # Convert Sales to float
        elif key == "Sales":
            if value:
                try:
                    transformed[key] = float(value)
                except (ValueError, TypeError) as e:
                    logger.warning(f"Order {order_id}: Could not convert Sales '{value}' to number - {e}")
                    transformed[key] = None
            else:
                transformed[key] = None
        
        # Keep other fields as they are
        else:
            transformed[key] = value
    
    return transformed
