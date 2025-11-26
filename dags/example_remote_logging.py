
from datetime import datetime
from airflow.decorators import dag, task

@dag(dag_id="example_remote_logging", start_date=datetime(2025,1,1), schedule=None, catchup=False)
def example_remote_logging():
    @task
    def run():
        print("Running example_remote_logging")
    run()

dag = example_remote_logging()
