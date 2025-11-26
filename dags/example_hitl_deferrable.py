
from datetime import datetime
from airflow.decorators import dag, task

@dag(dag_id="example_hitl_deferrable", start_date=datetime(2025,1,1), schedule=None, catchup=False)
def example_hitl_deferrable():
    @task
    def run():
        print("Running example_hitl_deferrable")
    run()

dag = example_hitl_deferrable()
