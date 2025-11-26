
from datetime import datetime
from airflow.decorators import dag, task

@dag(dag_id="example_schedule_variants", start_date=datetime(2025,1,1), schedule=None, catchup=False)
def example_schedule_variants():
    @task
    def run():
        print("Running example_schedule_variants")
    run()

dag = example_schedule_variants()
