# E-Commerce Analytics Ingestion Engine

A robust data ingestion pipeline for processing e-commerce order data from CSV files and loading it into MongoDB.

## 📁 Project Structure

```
e-commerce/
├── data/
│   ├── orders.csv              # Source CSV file with order data
│   └── checkpoint.json         # Checkpoint file for resume capability (gitignored)
├── logs/                       # Application logs (gitignored)
│   └── ingestion.log
├── services/
│   └── ingest-analytics-engine/
│       ├── main.py             # Main orchestration script
│       └── src/
│           ├── ingestion/      # Data ingestion modules
│           │   ├── reader.py      # CSV reader with checkpoint support
│           │   ├── validator.py   # Order validation module
│           │   ├── transformer.py # Data transformation module
│           │   └── loader.py      # MongoDB loader module
│           ├── analytics/     # Analytics modules
│           │   ├── yearly_growth.py
│           │   ├── monthly_trends.py
│           │   ├── category_intelligence.py
│           │   └── product_intelligence.py
│           └── utils/         # Shared utilities
│               ├── config.py      # Centralized configuration
│               └── logger.py     # Centralized logging setup
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variables template
├── .gitignore                # Git ignore rules
└── README.md                  # This file
```

## 🗂️ File Index

### Core Application Files

#### `services/ingest-analytics-engine/main.py`
**Purpose**: Main orchestration script that coordinates the entire ingestion pipeline.

**Features**:
- Reads checkpoint for resume capability
- Orchestrates reader → validator → transformer → loader pipeline
- Updates checkpoint after each successful batch
- Provides summary statistics
- Handles errors and interruptions gracefully

**Usage**:
```bash
cd services/ingest-analytics-engine
python3 main.py
```

#### `services/ingest-analytics-engine/src/ingestion/reader.py`
**Purpose**: Safely reads CSV files with checkpoint resume support.

**Key Functions**:
- `read_orders_csv(file_path, start_line)`: Streams rows as dictionaries
- `get_total_row_count(file_path)`: Returns total row count

**Features**:
- UTF-8 encoding handling
- Checkpoint resume (start from specific line)
- Streaming rows as dictionaries
- Logs row count

#### `services/ingest-analytics-engine/src/ingestion/validator.py`
**Purpose**: Validates order rows before insertion.

**Key Functions**:
- `validate_order(row)`: Returns `(True, cleaned_row)` or `(False, error_reason)`

**Validation Rules**:
- Required fields: Order ID, Order Date, Product ID, Category, Sub-Category, Sales
- Checks for missing/empty fields
- Strips whitespace from values
- Logs skipped rows to `./logs/ingestion.log`

#### `services/ingest-analytics-engine/src/ingestion/transformer.py`
**Purpose**: Normalizes validated order rows.

**Key Functions**:
- `transform_order(row)`: Returns transformed dictionary

**Transformations**:
- Converts Order Date and Ship Date to Python `datetime` objects
- Converts Sales to `float`
- Converts empty strings to `None`
- Logs conversion errors

#### `services/ingest-analytics-engine/src/ingestion/loader.py`
**Purpose**: Loads transformed rows into MongoDB.

**Key Functions**:
- `get_mongo_client()`: Creates MongoDB client from MONGO_URI
- `create_indexes(collection)`: Creates indexes on key fields
- `insert_batch_with_retry(collection, batch)`: Inserts batch with retry logic

**Features**:
- Connects using `MONGO_URI` environment variable
- Inserts in batches of 1000
- Creates indexes: Order ID, Product ID, Category, Order Date
- Handles retries (max 3 attempts with exponential backoff)
- Logs inserted/skipped counts

#### `services/ingest-analytics-engine/src/utils/config.py`
**Purpose**: Centralized configuration settings.

**Features**:
- All project settings in one place
- Paths, database names, batch sizes
- Environment variable loading
- Easy to modify and understand

#### `services/ingest-analytics-engine/src/utils/logger.py`
**Purpose**: Centralized logging setup.

**Features**:
- Consistent logging across all modules
- File-based logging to `logs/ingestion.log`
- Simple configuration

#### Analytics Modules
**Location**: `services/ingest-analytics-engine/src/analytics/`

- `yearly_growth.py`: Calculate yearly sales and growth percentage
- `monthly_trends.py`: Get monthly revenue trends
- `category_intelligence.py`: Average sales by category/sub-category
- `product_intelligence.py`: Top products by sales

### Configuration Files

#### `requirements.txt`
Python package dependencies:
- `pymongo>=4.0.0` - MongoDB driver
- `python-dotenv>=1.0.0` - Environment variable management

#### `.env`
Environment variables (not tracked in git):
```
MONGO_URI=mongodb+srv://user:password@cluster.mongodb.net/
```

### Data Files

#### `data/orders.csv`
Source CSV file with order data. Expected columns:
- Row ID, Order ID, Order Date, Ship Date, Ship Mode
- Customer ID, Customer Name, Segment
- Country, City, State, Postal Code, Region
- Product ID, Category, Sub-Category, Product Name
- Sales

#### `data/checkpoint.json`
Checkpoint file for resume capability:
```json
{
  "last_processed_line": 5000
}
```

### Log Files

#### `logs/ingestion.log`
Application logs with:
- Connection status
- Validation errors
- Transformation errors
- Batch insertion progress
- Summary statistics

## 🚀 Setup & Installation

### Prerequisites
- Python 3.7+
- MongoDB instance (local or Atlas)
- Access to `data/orders.csv`

### Installation Steps

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment**:
   Copy `.env.example` to `.env` and fill in your MongoDB connection string:
   ```bash
   cp .env.example .env
   # Edit .env and add your MONGO_URI
   ```
   
   Example `.env` content:
   ```
   MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/
   ```

3. **Run the ingestion**:
   ```bash
   cd services/ingest-analytics-engine
   python3 main.py
   ```

## 📊 Pipeline Flow

```
CSV File (orders.csv)
    ↓
[Reader] → Stream rows as dictionaries
    ↓
[Validator] → Check required fields, strip whitespace
    ↓
[Transformer] → Convert dates, convert Sales to float
    ↓
[Loader] → Batch insert into MongoDB (1000 rows/batch)
    ↓
MongoDB (ecommerce.orders collection)
```

## 🔧 Configuration

### MongoDB Configuration
- **Database**: `ecommerce`
- **Collection**: `orders`
- **Batch Size**: 1000 rows
- **Indexes**: Order ID, Product ID, Category, Order Date

### Checkpoint System
- Checkpoint file: `./data/checkpoint.json`
- Updated after each successful batch
- Allows resume from last processed line

### Logging
- Log file: `./logs/ingestion.log`
- Logs validation errors, transformation errors, and batch progress

## 📈 Usage Examples

### Run Full Ingestion
```bash
cd services/ingest-analytics-engine
python3 main.py
```

### Resume from Checkpoint
If interrupted, simply run again - it will automatically resume from the last checkpoint.

### Check Logs
```bash
tail -f logs/ingestion.log
```

## 🛠️ Troubleshooting

### MongoDB Connection Issues
- Verify `MONGO_URI` in `.env` file
- Check MongoDB network access/firewall
- For Atlas: Ensure IP whitelist includes your IP

### CSV File Not Found
- Ensure `data/orders.csv` exists in project root
- Check file path in error message

### Validation Errors
- Check `logs/ingestion.log` for specific validation failures
- Ensure CSV has all required columns

## 📝 Summary Statistics

After completion, the script displays:
- Total rows processed
- Valid rows
- Invalid rows
- Inserted rows
- Skipped rows

## 🔒 Security Notes

- `.env` file is gitignored and should not be committed to version control
- MongoDB credentials should be kept secure
- SSL/TLS is enabled for MongoDB Atlas connections
- Use `.env.example` as a template for setting up your environment

## 📦 Git Setup

The project includes a `.gitignore` file that excludes:
- Environment files (`.env`)
- Python cache files (`__pycache__/`, `*.pyc`)
- Log files (`logs/`)
- Checkpoint files (`data/checkpoint.json`)
- IDE files (`.vscode/`, `.idea/`)
- Virtual environments (`venv/`, `env/`)

To commit the project:
```bash
git init
git add .
git commit -m "Initial commit: E-commerce analytics ingestion engine"
```

## 📚 Module Dependencies

```
main.py
├── reader.py (csv, logging, pathlib)
├── validator.py (logging, pathlib, typing)
├── transformer.py (logging, datetime, pathlib, typing)
└── loader.py (pymongo, logging, pathlib, typing, dotenv)
```

## 🎯 Key Features

- ✅ Checkpoint resume capability
- ✅ Batch processing (1000 rows/batch)
- ✅ Comprehensive validation
- ✅ Data type transformation
- ✅ Error handling and retries
- ✅ Detailed logging
- ✅ Progress tracking
- ✅ Summary statistics

