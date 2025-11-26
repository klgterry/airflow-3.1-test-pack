
from datetime import datetime
from airflow.decorators import dag, task

@dag(dag_id="example_xcom_large_payload", start_date=datetime(2025,1,1), schedule=None, catchup=False)
def example_xcom_large_payload():
    @task
    def run():
        print("Running example_xcom_large_payload")
    run()

dag = example_xcom_large_payload()
