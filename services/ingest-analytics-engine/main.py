"""
Main script to process orders from CSV and load them into MongoDB.

The flow is simple:
1. Read checkpoint (where we left off)
2. Connect to MongoDB
3. For each row in CSV:
   - Validate it
   - Transform it
   - Add to batch
   - When batch is full, save to database
4. Show summary
"""

import json
import sys
from pathlib import Path
from typing import Dict, Any, List

# Add src to path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent / "src"))

from ingestion.reader import read_orders_csv
from ingestion.validator import validate_order
from ingestion.transformer import transform_order
from ingestion.loader import get_mongo_client, create_indexes, insert_batch_with_retry
from utils.config import CHECKPOINT_FILE, CSV_FILE, BATCH_SIZE, DATABASE_NAME, COLLECTION_NAME
from utils.logger import get_logger

logger = get_logger(__name__)


def read_checkpoint() -> int:
    """
    Read the checkpoint file to see where we left off.
    
    Returns:
        Line number to resume from (0 = start from beginning)
    """
    if not CHECKPOINT_FILE.exists():
        logger.info("No checkpoint found, starting from beginning")
        return 0
    
    try:
        with open(CHECKPOINT_FILE, 'r') as f:
            data = json.load(f)
            line_number = data.get("last_processed_line", 0)
            logger.info(f"Resuming from line {line_number}")
            return line_number
    except Exception as e:
        logger.warning(f"Could not read checkpoint: {e}. Starting from beginning.")
        return 0


def save_checkpoint(line_number: int):
    """
    Save our progress so we can resume later if needed.
    
    Args:
        line_number: Last line we successfully processed
    """
    try:
        CHECKPOINT_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(CHECKPOINT_FILE, 'w') as f:
            json.dump({"last_processed_line": line_number}, f, indent=2)
    except Exception as e:
        logger.error(f"Could not save checkpoint: {e}")


def main():
    """
    Main function: process all orders from CSV to MongoDB.
    """
    # Track statistics
    total_rows = 0
    valid_rows = 0
    invalid_rows = 0
    inserted_rows = 0
    skipped_rows = 0
    
    client = None
    
    try:
        # Step 1: Read checkpoint to see where we left off
        start_line = read_checkpoint()
        
        # Step 2: Connect to MongoDB
        logger.info("Connecting to MongoDB...")
        client = get_mongo_client()
        db = client[DATABASE_NAME]
        collection = db[COLLECTION_NAME]
        
        # Step 3: Create indexes for faster queries
        logger.info("Creating indexes...")
        create_indexes(collection)
        
        # Step 4: Process each row from CSV
        logger.info("Starting to process orders...")
        batch = []
        current_line = start_line
        
        for row in read_orders_csv(file_path=str(CSV_FILE), start_line=start_line):
            total_rows += 1
            current_line = start_line + total_rows
            
            # Validate the row
            is_valid, result = validate_order(row)
            if not is_valid:
                invalid_rows += 1
                continue  # Skip invalid rows
            
            # Transform the row (convert dates, numbers, etc.)
            validated_row = result
            transformed_row = transform_order(validated_row)
            valid_rows += 1
            
            # Add to batch
            batch.append(transformed_row)
            
            # When batch is full, save it to database
            if len(batch) >= BATCH_SIZE:
                inserted, skipped = insert_batch_with_retry(collection, batch)
                inserted_rows += inserted
                skipped_rows += skipped
                
                # Save checkpoint after each successful batch
                save_checkpoint(current_line - 1)
                logger.info(f"Processed batch: {inserted} inserted, {skipped} skipped")
                
                batch = []  # Reset batch
        
        # Step 5: Save any remaining rows in the batch
        if batch:
            inserted, skipped = insert_batch_with_retry(collection, batch)
            inserted_rows += inserted
            skipped_rows += skipped
            save_checkpoint(current_line - 1)
            logger.info(f"Processed final batch: {inserted} inserted, {skipped} skipped")
        
        # Step 6: Show summary
        print("\n" + "=" * 50)
        print("INGESTION SUMMARY")
        print("=" * 50)
        print(f"Total rows processed:    {total_rows}")
        print(f"Valid rows:              {valid_rows}")
        print(f"Invalid rows:            {invalid_rows}")
        print(f"Inserted rows:           {inserted_rows}")
        print(f"Skipped rows:            {skipped_rows}")
        print("=" * 50 + "\n")
        
        logger.info(f"Done! Processed {total_rows} rows, inserted {inserted_rows}")
    
    except KeyboardInterrupt:
        logger.warning("Process interrupted by user")
        print("\nProcess interrupted. Progress saved - you can resume later.")
        sys.exit(1)
    
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        print(f"\nError occurred: {e}")
        print("Check logs for details.")
        sys.exit(1)
    
    finally:
        # Always close the database connection
        if client:
            client.close()
            logger.info("Closed MongoDB connection")

if __name__ == "__main__":
    main()
