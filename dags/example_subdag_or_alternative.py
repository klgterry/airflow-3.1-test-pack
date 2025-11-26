
from datetime import datetime
from airflow.decorators import dag, task

@dag(dag_id="example_subdag_or_alternative", start_date=datetime(2025,1,1), schedule=None, catchup=False)
def example_subdag_or_alternative():
    @task
    def run():
        print("Running example_subdag_or_alternative")
    run()

dag = example_subdag_or_alternative()
