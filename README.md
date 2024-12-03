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
- `heading`: The required column

**Example Request:**

```
GET /data?startTime=2023-01-01T00:00:00&endTime=2023-12-31T23:59:59
```

### GET `/trend`

Calculate trends over a specified period.

**Parameters:**

- `window`: Time window (e.g., 7d, 2h, 1m)
- `startTime`: Start timestamp (ISO format)
- `heading`: The required column
- `datapoints`: Boolean if datapoints are required

**Example Request:**

```
GET /trend?window=2h&heading=CO(GT)&startTime=2004-03-10T19:00:00&datapoints=true
```

### GET `/trend-compare`

Compares trends of two windows.

**Parameters:**

- `window`: Time window (e.g., 7d, 2h, 1m)
- `startTime1`: Start timestamp (ISO format)
- `startTime2`: Start timestamp (ISO format)
- `heading`: The required column
- `datapoints`: Boolean if datapoints are required

**Example Request:**

```
GET /trend-compare?window=2h&heading=CO(GT)&startTime1=2004-03-10T19:00:00&startTime2=2004-03-13T03:00:00
```
