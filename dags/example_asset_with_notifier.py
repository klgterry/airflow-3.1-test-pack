
from datetime import datetime
from airflow.decorators import dag, task

@dag(dag_id="example_asset_with_notifier", start_date=datetime(2025,1,1), schedule=None, catchup=False)
def example_asset_with_notifier():
    @task
    def run():
        print("Running example_asset_with_notifier")
    run()

dag = example_asset_with_notifier()
