
from datetime import datetime
from airflow.decorators import dag, task

@dag(dag_id="example_deadline_with_slack", start_date=datetime(2025,1,1), schedule=None, catchup=False)
def example_deadline_with_slack():
    @task
    def run():
        print("Running example_deadline_with_slack")
    run()

dag = example_deadline_with_slack()
