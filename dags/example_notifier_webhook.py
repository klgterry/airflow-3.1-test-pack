
from datetime import datetime
from airflow.decorators import dag, task

@dag(dag_id="example_notifier_webhook", start_date=datetime(2025,1,1), schedule=None, catchup=False)
def example_notifier_webhook():
    @task
    def run():
        print("Running example_notifier_webhook")
    run()

dag = example_notifier_webhook()
