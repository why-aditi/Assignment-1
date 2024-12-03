# Time Series Data Analysis API

## Project Overview

A Flask-based API for efficient time series data retrieval and trend analysis using MongoDB.

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

### 4. Run the Application

```bash
python main.py
```

## API Endpoints

### GET `/data`

Retrieve time series data for a specific time range.

**Parameters:**
- `startTime`: Start timestamp (ISO format)
- `endTime`: End timestamp (ISO format)

**Example Request:**

```
GET /data?startTime=2023-01-01T00:00:00Z&endTime=2023-12-31T23:59:59Z
```

### GET `/trend`

Calculate trends over a specified period.

**Parameters:**
- `window`: Time window (e.g., 7d, 2h, 1m)

**Example Request:**

```
GET /trend?window=7d
```
