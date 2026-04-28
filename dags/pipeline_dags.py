from airflow.sdk import dag, task
import pendulum
from datetime import datetime, timedelta
from data_ingestion.fetch_data import fetch_and_save

@dag(
        dag_id='data_pipeline',
        schedule="0 6 * * *",
        start_date=pendulum.datetime(2026, 4, 11, tz="UTC"),
        catchup=False
)

def data_pipeline():

    @task.python
    def fetch_raw_data():
        fetch_and_save()


    fetch_raw_data()
    @task()
    def run_dbt():
        import subprocess
        result = subprocess.run(
            ["dbt", "run", 
             "--project-dir", "/opt/airflow/finance_dbt",
             "--profiles-dir", "/opt/airflow/finance_dbt"],
            capture_output=True,
            text=True
        )
        print(result.stdout)
        print(result.stderr)
        if result.returncode != 0:
            raise Exception(f"dbt run failed: {result.stderr}")

    @task()
    def run_dbt_tests():
        import subprocess
        result = subprocess.run(
            ["dbt", "test",
             "--project-dir", "/opt/airflow/finance_dbt",
             "--profiles-dir", "/opt/airflow/finance_dbt"],
            capture_output=True,
            text=True
        )
        print(result.stdout)
        if result.returncode != 0:
            raise Exception(f"dbt test failed: {result.stderr}")

    @task()
    def export_to_s3():
        from data_ingestion.export_to_s3 import export_to_s3 as run_export
        run_export()

    # Pipeline order
    fetch_raw_data() >> run_dbt() >> run_dbt_tests() >> export_to_s3()

data_pipeline_dag = data_pipeline()

 


