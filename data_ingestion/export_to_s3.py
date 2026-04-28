import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
from datetime import datetime
import os
import boto3
import io

load_dotenv()

engine = create_engine(
    f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
)

s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION')
)

def export_to_s3():
    today = datetime.now().strftime('%Y-%m-%d')

    tables = {
        "daily_returns": "transformed/daily_returns",
        "price_summary": "transformed/price_summary"
    }

    for table, s3_path in tables.items():
        df = pd.read_sql(f"SELECT * FROM public.{table}", engine)
        print(f"✅ {table} — {len(df)} rows read from Postgres")

        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)

        file_name = f"{s3_path}_{today}.csv"
        s3_client.put_object(
            Bucket=os.getenv('AWS_BUCKET_NAME'),
            Key=file_name,
            Body=csv_buffer.getvalue()
        )
        print(f"✅ {table} saved to S3: {file_name}")


if __name__ == "__main__":
    export_to_s3()