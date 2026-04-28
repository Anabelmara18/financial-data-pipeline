# Financial Data Pipeline 

End-to-end financial data pipeline tracking Tech Giants & Crypto — built with Apache Airflow, dbt, PostgreSQL, AWS S3, and Apache Superset.

## Overview
This pipeline automatically fetches daily stock and cryptocurrency data for 7 assets (AAPL, GOOGL, MSFT, NVDA, BTC-USD, ETH-USD, SOL-USD), transforms it using dbt, stores it in PostgreSQL, exports to AWS S3, and visualizes it in Apache Superset.

## Architecture
yfinance API → Apache Airflow → PostgreSQL → dbt → AWS S3 → Apache Superset

## Tech Stack
- **Orchestration:** Apache Airflow 3.2.0
- **Transformation:** dbt Core 1.9.0
- **Database:** PostgreSQL 16
- **Cloud Storage:** AWS S3
- **Visualization:** Apache Superset 3.1.0
- **Containerization:** Docker & Docker Compose
- **Language:** Python 3.13

## Assets Tracked
| Asset | Type |
|-------|------|
| AAPL | Stock |
| GOOGL | Stock |
| MSFT | Stock |
| NVDA | Stock |
| BTC-USD | Crypto |
| ETH-USD | Crypto |
| SOL-USD | Crypto |

## Pipeline Flow
1. **Fetch** — Airflow fetches daily OHLCV data from yfinance
2. **Store** — Raw data stored in PostgreSQL
3. **Transform** — dbt builds staging and mart models
4. **Test** — dbt runs data quality tests
5. **Export** — Transformed data exported to AWS S3
6. **Visualize** — Apache Superset reads from PostgreSQL

## dbt Models
- `stg_stock_price` — staging model cleaning raw data
- `daily_returns` — calculates daily return % per asset
- `price_summary` — all time high/low, avg close, avg volume per asset

## Setup
1. Clone the repo
```bash
git clone https://github.com/Anabelmara18/financial-data-pipeline.git
cd financial-data-pipeline
```

2. Copy environment file
```bash
cp .env.example .env
```

3. Fill in your credentials in `.env`

4. Start the pipeline
```bash
docker compose up -d
```

5. Access Airflow at `http://localhost:8080`
6. Access Superset at `http://localhost:8088`

## Dashboard
The Superset dashboard shows:
- Latest prices for all 7 assets (KPI cards)
- Price trends over time (line charts)
- Daily returns % (bar chart)
- Volume distribution (pie charts)
- Monthly return heatmap

## Project Structure

```text
financial-data-pipeline/
├── dags/                    # Airflow DAG
├── data_ingestion/          # Fetch & export scripts
├── finance_dbt/             # dbt project
│   └── models/
│       ├── staging_models/
│       └── mart_models/
├── docker-compose.yaml      # Docker setup
├── .env.example             # Environment template
└── README.md
```
