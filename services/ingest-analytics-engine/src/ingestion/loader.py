"""
Loads order data into MongoDB.
Handles connections, creates indexes, and inserts data in batches.
"""

import time
from typing import Dict, Any, List, Tuple
from pymongo import MongoClient
from pymongo.errors import BulkWriteError, ConnectionFailure
from utils.logger import get_logger
from utils.config import MONGO_URI, DATABASE_NAME, COLLECTION_NAME, MAX_RETRIES, RETRY_DELAY

logger = get_logger(__name__)


def get_mongo_client() -> MongoClient:
    """
    Connect to MongoDB using the connection string.
    
    Returns:
        MongoDB client connection
    """
    if not MONGO_URI:
        raise ValueError("MONGO_URI environment variable is not set. Please check your .env file.")
    
    try:
        client = MongoClient(MONGO_URI, tlsAllowInvalidCertificates=True)
        # Test the connection
        client.admin.command('ping')
        logger.info("Connected to MongoDB successfully")
        return client
    except ConnectionFailure as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        raise


def create_indexes(collection):
    """
    Create indexes on important fields to speed up queries.
    
    Args:
        collection: MongoDB collection object
    """
    indexes = [
        ("Order ID", 1),
        ("Product ID", 1),
        ("Category", 1),
        ("Order Date", 1),
    ]
    
    for field, direction in indexes:
        try:
            collection.create_index([(field, direction)])
            logger.info(f"Created index on {field}")
        except Exception as e:
            logger.warning(f"Could not create index on {field}: {e}")


def insert_batch_with_retry(collection, batch: List[Dict[str, Any]], retry_count: int = 0) -> Tuple[int, int]:
    """
    Insert a batch of orders into MongoDB.
    If it fails, retry a few times before giving up.
    
    Args:
        collection: MongoDB collection object
        batch: List of order dictionaries to insert
        retry_count: How many times we've tried already
    
    Returns:
        (number_inserted, number_skipped)
    """
    if not batch:
        return 0, 0
    
    try:
        # Try to insert all documents
        result = collection.insert_many(batch, ordered=False)
        inserted = len(result.inserted_ids)
        skipped = len(batch) - inserted
        return inserted, skipped
    
    except BulkWriteError as e:
        # Some documents might have been inserted
        inserted = len(e.details.get('insertedIds', []))
        skipped = len(batch) - inserted
        
        # Retry if we haven't exceeded max retries
        if retry_count < MAX_RETRIES:
            wait_time = RETRY_DELAY * (retry_count + 1)
            logger.warning(f"Batch insert had errors. Retrying in {wait_time} seconds... (attempt {retry_count + 1}/{MAX_RETRIES})")
            time.sleep(wait_time)
            return insert_batch_with_retry(collection, batch, retry_count + 1)
        else:
            logger.error(f"Batch insert failed after {MAX_RETRIES} retries. Inserted: {inserted}, Skipped: {skipped}")
            return inserted, skipped
    
    except Exception as e:
        # Other errors - retry if possible
        if retry_count < MAX_RETRIES:
            wait_time = RETRY_DELAY * (retry_count + 1)
            logger.warning(f"Batch insert error: {e}. Retrying in {wait_time} seconds... (attempt {retry_count + 1}/{MAX_RETRIES})")
            time.sleep(wait_time)
            return insert_batch_with_retry(collection, batch, retry_count + 1)
        else:
            logger.error(f"Batch insert failed after {MAX_RETRIES} retries: {e}")
            return 0, len(batch)
