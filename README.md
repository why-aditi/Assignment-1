# Time Series Data Analysis API

## Project Overview

A Flask-based API for efficient time series data retrieval and trend analysis using MongoDB.

## Prerequisites

- Python 3.9+
- MongoDB 5.0+

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/why-aditi/Time-Series-Flask-Analysis.git
cd Time-Series-Flask-Analysis
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure MongoDB

- Install MongoDB locally or use a cloud service
- Create a `.env` file with your MongoDB connection string

```
MONGO_URI=mongodb://localhost:27017
DATABASE_NAME=timeseries_db
```

### 5. Run the Application

```bash
python app.py
```

## API Endpoints

### GET `/data`

Retrieve time series data for a specific time range.

**Parameters:**

- `collection`: Name of MongoDB collection
- `uid`: Unique identifier for filtering
- `startTime`: Start timestamp (ISO format)
- `endTime`: End timestamp (ISO format)

**Example Request:**

```
GET /data?collection=stockPrices&uid=AAPL&startTime=2023-01-01T00:00:00Z&endTime=2023-12-31T23:59:59Z
```

### GET `/trend`

Calculate trends over a specified period.

**Parameters:**

- `collection`: Name of MongoDB collection
- `window`: Time window (e.g., 7d, 2h, 1m)

**Example Request:**

```
GET /trend?collection=stockPrices&window=7d
```
