"""
Reads order data from CSV file.
Supports resuming from a specific line number (checkpoint).
"""

import csv
from pathlib import Path
from typing import Iterator, Dict
from utils.logger import get_logger
from utils.config import CSV_FILE

logger = get_logger(__name__)


def read_orders_csv(file_path: str = None, start_line: int = 0) -> Iterator[Dict[str, str]]:
    """
    Read CSV file and return each row as a dictionary.
    
    Args:
        file_path: Path to CSV file. Uses default if not provided.
        start_line: Line number to start from (skip earlier lines).
    
    Yields:
        Dictionary with column names as keys.
    """
    # Use default file path if not provided
    if file_path is None:
        file_path = str(CSV_FILE)
    
    csv_path = Path(file_path)
    
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {file_path}")
    
    logger.info(f"Reading CSV file: {csv_path}")
    
    # Open file and read rows
    with open(csv_path, 'r', encoding='utf-8', errors='replace') as file:
        reader = csv.DictReader(file)
        
        # Skip rows until we reach the start line
        for _ in range(start_line):
            try:
                next(reader)
            except StopIteration:
                logger.info("Reached end of file while skipping rows")
                return
        
        # Read and yield each row
        row_count = 0
        for row in reader:
            row_count += 1
            yield row
        
        logger.info(f"Finished reading {row_count} rows from CSV")
