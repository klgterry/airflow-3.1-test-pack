
from __future__ import annotations
from datetime import datetime

from airflow.decorators import dag, task


@dag(
    dag_id="example_deadline_alert",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["deadline"],
)
def example_deadline_alert():
    """Simplified Deadline-like example.

    This does NOT use the new DeadlineAlert API directly (for portability),
    but simulates a long-running DAG run you can monitor with your own alerts.
    """ 

    @task
    def long_task():
        import time
        print("Starting long task...")
        time.sleep(60)
        print("Long task finished.")

    long_task()


dag = example_deadline_alert()
