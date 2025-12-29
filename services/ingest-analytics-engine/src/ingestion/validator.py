"""
Validates order data before processing.
Checks that all required fields are present and not empty.
"""

from typing import Dict, Tuple, Any
from utils.logger import get_logger
from utils.config import REQUIRED_FIELDS

logger = get_logger(__name__)


def validate_order(row: Dict[str, Any]) -> Tuple[bool, Any]:
    """
    Check if an order row has all required fields.
    
    Args:
        row: Dictionary with order data
    
    Returns:
        (True, cleaned_row) if valid, (False, error_message) if invalid
    """
    # Make sure we have a dictionary
    if not isinstance(row, dict):
        error = "Row is not a dictionary"
        logger.warning(f"Validation failed: {error}")
        return False, error
    
    # Clean up the row: remove extra whitespace from strings
    cleaned_row = {}
    for key, value in row.items():
        if isinstance(value, str):
            cleaned_row[key] = value.strip()
        else:
            cleaned_row[key] = value
    
    # Check each required field
    missing_fields = []
    empty_fields = []
    
    for field in REQUIRED_FIELDS:
        if field not in cleaned_row:
            missing_fields.append(field)
        elif not cleaned_row[field]:
            empty_fields.append(field)
    
    # If any fields are missing or empty, validation fails
    if missing_fields or empty_fields:
        error_parts = []
        if missing_fields:
            error_parts.append(f"missing: {', '.join(missing_fields)}")
        if empty_fields:
            error_parts.append(f"empty: {', '.join(empty_fields)}")
        
        error_message = f"Validation failed - {', '.join(error_parts)}"
        order_id = cleaned_row.get("Order ID", "unknown")
        logger.warning(f"Order {order_id}: {error_message}")
        return False, error_message
    
    # All checks passed
    return True, cleaned_row
