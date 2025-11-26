
from datetime import datetime
from airflow.decorators import dag, task

@dag(dag_id="example_sensor_branch_trigger", start_date=datetime(2025,1,1), schedule=None, catchup=False)
def example_sensor_branch_trigger():
    @task
    def run():
        print("Running example_sensor_branch_trigger")
    run()

dag = example_sensor_branch_trigger()
