
from datetime import datetime
from airflow.decorators import dag, task

@dag(dag_id="example_deferrable_timeout_retry", start_date=datetime(2025,1,1), schedule=None, catchup=False)
def example_deferrable_timeout_retry():
    @task
    def run():
        print("Running example_deferrable_timeout_retry")
    run()

dag = example_deferrable_timeout_retry()
