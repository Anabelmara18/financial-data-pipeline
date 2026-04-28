
import yfinance as yf
import psycopg2
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
import os
import time

load_dotenv()

# Database connection parameters from environment variables
engine = create_engine(
    f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
)


tickers = ["AAPL", "GOOGL", "MSFT", "NVDA", "BTC-USD", "ETH-USD", "SOL-USD"]

def fetch_and_save():
    today_utc = datetime.now(timezone.utc)

    yesterday = (today_utc - timedelta(days=1)).strftime('%Y-%m-%d')
    today = (today_utc).strftime('%Y-%m-%d')

    all_data = []

    for ticker in tickers:
        df = yf.download(
            ticker,
            start=yesterday,
            end=today,
            auto_adjust=True,
            progress=False
        )

        

        if df.empty:
            print(f"⚠️ No data for {ticker} — skipping")
        else:
            df = df.reset_index()
            df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]
            df = df[["Date", "Open", "High", "Low", "Close", "Volume"]]
            df.columns = ["date", "open", "high", "low", "close", "volume"]
            df["ticker"] = ticker
            df["ingested_at"] = datetime.now()
            all_data.append(df)

            time.sleep(1.5)
        
    if not all_data:
        print("⚠️ No data fetched today — market might be closed")
        return

    final_df = pd.concat(all_data, ignore_index=True)
    print(final_df.shape)


    final_df.to_sql('finance_data', engine, if_exists='append', index=False)
    print("✅ Data saved to Postgres")
    

if __name__ == "__main__":
    fetch_and_save()

