# E-Commerce Analytics Platform

A complete, production-ready e-commerce analytics platform with data ingestion, RESTful API, and modern web UI. The platform processes order data from CSV files, stores it in MongoDB, and provides real-time analytics through a React-based dashboard.

## 🏗️ Architecture

The platform consists of three microservices orchestrated via Docker Compose:

```
┌─────────────────┐
│   UI Service    │ (React + Nginx) - Port 80
│   (Frontend)    │
└────────┬────────┘
         │ HTTP
         ▼
┌─────────────────┐
│  API Service     │ (Flask) - Port 5000
│  (Backend)       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   MongoDB       │ - Port 27017
│   (Database)    │
└─────────────────┘
         ▲
         │
┌────────┴────────┐
│ Ingest Engine   │ (Python Script)
│ (Data Pipeline) │
└─────────────────┘
```

## 📁 Project Structure

```
e-commerce/
├── data/
│   └── orders.csv              # Source CSV file with order data
├── logs/                       # Application logs (gitignored)
├── services/
│   ├── ingest-analytics-engine/
│   │   ├── Dockerfile
│   │   ├── main.py             # Main orchestration script
│   │   └── src/
│   │       ├── ingestion/      # Data ingestion modules
│   │       │   ├── reader.py      # CSV reader with checkpoint support
│   │       │   ├── validator.py   # Order validation module
│   │       │   ├── transformer.py # Data transformation module
│   │       │   └── loader.py      # MongoDB loader module
│   │       ├── analytics/      # Analytics modules
│   │       │   ├── product_intelligence.py
│   │       │   ├── monthly_trends.py
│   │       │   ├── category_intelligence.py
│   │       │   └── yearly_growth.py
│   │       └── utils/          # Shared utilities
│   │           ├── config.py      # Centralized configuration
│   │           └── logger.py     # Centralized logging setup
│   ├── api-service/
│   │   ├── Dockerfile
│   │   └── app.py              # Flask API service
│   └── ui-service/
│       ├── Dockerfile
│       ├── nginx.conf
│       ├── package.json
│       ├── tailwind.config.js
│       ├── postcss.config.js
│       ├── public/            # Static assets
│       └── src/
│           ├── pages/          # React pages
│           ├── components/    # React components
│           └── services/       # API client
├── docker-compose.yml          # Service orchestration
├── requirements.txt            # Python dependencies
├── env.template                # Environment variables template
├── .gitignore                  # Git ignore rules
├── LICENSE                     # License file
└── README.md                   # This file
```

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose installed
- Access to `data/orders.csv` file

### Installation & Running

1. **Clone the repository** (if applicable):
   ```bash
   git clone <repository-url>
   cd e-commerce
   ```

2. **Set up environment variables**:
   ```bash
   cp env.template .env
   # Edit .env with your configuration (optional - defaults work for Docker)
   ```

3. **Start all services**:
   ```bash
   docker-compose up -d
   ```

4. **View logs**:
   ```bash
   docker-compose logs -f
   ```

5. **Access the application**:
   - **UI Dashboard**: http://localhost
   - **API**: http://localhost:5000
   - **API Health Check**: http://localhost:5000/api/health

6. **Stop all services**:
   ```bash
   docker-compose down
   ```

## 🎯 Services Overview

### 1. Ingest Analytics Engine

**Purpose**: Processes CSV order data and loads it into MongoDB with analytics calculations.

**Features**:
- ✅ CSV file reading with checkpoint support
- ✅ Order validation and data transformation
- ✅ Batch insertion to MongoDB (1000 rows/batch)
- ✅ Analytics calculations:
  - Top products by sales
  - Monthly revenue trends
  - Category/subcategory averages
  - Yearly growth calculations
- ✅ Error handling with retry logic
- ✅ Comprehensive logging
- ✅ Resume capability from checkpoints

**Location**: `services/ingest-analytics-engine/`

### 2. API Service

**Purpose**: RESTful API service providing analytics data endpoints.

**Endpoints**:
- `GET /api/analytics/top-products` - Top products by sales
- `GET /api/analytics/monthly-revenue` - Monthly revenue data
- `GET /api/analytics/category-avg-sales` - Category averages
- `GET /api/analytics/yearly-growth` - Yearly growth data
- `GET /api/health` - Health check endpoint

**Features**:
- ✅ CORS enabled for frontend access
- ✅ Error handling with proper HTTP status codes
- ✅ MongoDB connection management
- ✅ Logging integration

**Location**: `services/api-service/`

**Technology**: Flask (Python 3.11)

### 3. UI Service

**Purpose**: Modern web dashboard for visualizing analytics data.

**Pages**:
- `/` - Overview Dashboard
  - Top Products count
  - Total revenue (latest year)
  - Latest growth percentage
- `/products` - Top Products Table
- `/categories` - Category Analytics
- `/trends` - Sales Trends (Monthly Revenue & Yearly Growth)

**Features**:
- ✅ React Router for navigation
- ✅ Axios for API calls
- ✅ Tailwind CSS for styling
- ✅ Loading states and error handling
- ✅ Responsive design
- ✅ API health indicator (auto-refreshes every 30s)

**Location**: `services/ui-service/`

**Technology**: React 19 + Tailwind CSS + Nginx

## 📊 Data Flow

```
1. CSV Data (orders.csv)
   ↓
2. Ingest Engine processes & validates
   ↓
3. MongoDB stores orders
   ↓
4. Analytics modules calculate metrics
   ↓
5. API Service exposes endpoints
   ↓
6. UI Service displays visualizations
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file from `env.template`:

```bash
cp env.template .env
```

**Key Variables**:
- `MONGO_URI` - MongoDB connection string (default: `mongodb://mongodb:27017/`)
- `DATABASE_NAME` - Database name (default: `ecommerce`)
- `COLLECTION_NAME` - Collection name (default: `orders`)
- `API_PORT` - API service port (default: `5000`)
- `UI_PORT` - UI service port (default: `80`)
- `BATCH_SIZE` - Batch size for ingestion (default: `1000`)

See `env.template` for all available options.

### MongoDB Configuration

- **Database**: `ecommerce`
- **Collection**: `orders`
- **Indexes**: Order ID, Product ID, Category, Order Date
- **Batch Size**: 1000 rows

## 📦 Dependencies

### Python (`requirements.txt`)
- `pymongo>=4.0.0` - MongoDB driver
- `python-dotenv>=1.0.0` - Environment variables
- `flask>=2.0.0` - Web framework
- `flask-cors>=3.0.0` - CORS support

### Node.js (`services/ui-service/package.json`)
- `react@^19.2.3`
- `react-dom@^19.2.3`
- `react-router-dom@^6.30.2`
- `axios@^1.13.2`
- `tailwindcss@^3.4.0`

## 🐳 Docker Services

### MongoDB
- **Image**: `mongo:7`
- **Port**: `27017`
- **Volume**: Persistent data storage
- **Health Check**: Enabled

### Ingest Analytics Engine
- **Depends on**: MongoDB
- **Volumes**: `./data`, `./logs`
- **Restart**: on-failure

### API Service
- **Port**: `5000`
- **Depends on**: MongoDB
- **Restart**: unless-stopped

### UI Service
- **Port**: `80`
- **Depends on**: API service
- **Restart**: unless-stopped

## 🛠️ Development

### Running Services Individually

#### Ingest Engine
```bash
cd services/ingest-analytics-engine
python3 main.py
```

#### API Service
```bash
cd services/api-service
python3 app.py
```

#### UI Service
```bash
cd services/ui-service
npm install
npm start
```

### Local Development Setup

1. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Install Node.js dependencies**:
   ```bash
   cd services/ui-service
   npm install
   ```

3. **Set up MongoDB** (local or use Docker):
   ```bash
   docker run -d -p 27017:27017 --name mongodb mongo:7
   ```

4. **Configure environment**:
   ```bash
   cp env.template .env
   # Edit .env with your settings
   ```

## 📈 Usage Examples

### Check API Health
```bash
curl http://localhost:5000/api/health
```

### Get Top Products
```bash
curl http://localhost:5000/api/analytics/top-products
```

### Get Monthly Revenue
```bash
curl http://localhost:5000/api/analytics/monthly-revenue
```

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f api-service
docker-compose logs -f ingest-analytics-engine
```

## 🛠️ Troubleshooting

### MongoDB Connection Issues
- Verify `MONGO_URI` in `.env` file
- Check MongoDB container is running: `docker-compose ps`
- Check MongoDB health: `docker-compose logs mongodb`

### API Not Responding
- Check API service logs: `docker-compose logs api-service`
- Verify API service is running: `docker-compose ps`
- Test health endpoint: `curl http://localhost:5000/api/health`

### UI Not Loading
- Check UI service logs: `docker-compose logs ui-service`
- Verify API service is accessible from UI
- Check browser console for errors

### Data Ingestion Issues
- Check ingestion logs: `docker-compose logs ingest-analytics-engine`
- Verify `data/orders.csv` exists
- Check MongoDB connection and permissions

## 🔒 Security Notes

- `.env` file is gitignored and should not be committed
- MongoDB credentials should be kept secure
- Use environment variables for sensitive configuration
- SSL/TLS recommended for production MongoDB connections

## 📝 Git Setup

The project includes a `.gitignore` file that excludes:
- Environment files (`.env`)
- Python cache files (`__pycache__/`, `*.pyc`)
- Log files (`logs/`)
- Checkpoint files (`data/checkpoint.json`)
- Node modules (`node_modules/`)
- IDE files (`.vscode/`, `.idea/`)
- Virtual environments (`venv/`, `env/`)

## 🎯 Key Features

- ✅ Complete microservices architecture
- ✅ Docker containerization for all services
- ✅ Checkpoint resume capability for data ingestion
- ✅ Batch processing (1000 rows/batch)
- ✅ Comprehensive validation and error handling
- ✅ Real-time analytics dashboard
- ✅ RESTful API with CORS support
- ✅ Health check endpoints
- ✅ Detailed logging
- ✅ Production-ready configuration

## 📚 License

See `LICENSE` file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Support

For issues and questions, please check the logs first:
```bash
docker-compose logs -f
```

---

**Status**: ✅ Production Ready

All core components are implemented, tested, and containerized. The system is ready for deployment and can handle data ingestion, analytics calculations, RESTful API access, and modern web UI with real-time updates.
