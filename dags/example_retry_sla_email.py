
from datetime import datetime
from airflow.decorators import dag, task

@dag(dag_id="example_retry_sla_email", start_date=datetime(2025,1,1), schedule=None, catchup=False)
def example_retry_sla_email():
    @task
    def run():
        print("Running example_retry_sla_email")
    run()

dag = example_retry_sla_email()
