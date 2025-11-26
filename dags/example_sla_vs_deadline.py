
from datetime import datetime
from airflow.decorators import dag, task

@dag(dag_id="example_sla_vs_deadline", start_date=datetime(2025,1,1), schedule=None, catchup=False)
def example_sla_vs_deadline():
    @task
    def run():
        print("Running example_sla_vs_deadline")
    run()

dag = example_sla_vs_deadline()
