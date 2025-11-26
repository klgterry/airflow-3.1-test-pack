
from datetime import datetime
from airflow.decorators import dag, task

@dag(dag_id="example_hitl_required_actions_view", start_date=datetime(2025,1,1), schedule=None, catchup=False)
def example_hitl_required_actions_view():
    @task
    def run():
        print("Running example_hitl_required_actions_view")
    run()

dag = example_hitl_required_actions_view()
