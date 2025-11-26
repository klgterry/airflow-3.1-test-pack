
from __future__ import annotations
from datetime import datetime

from airflow.decorators import dag, task


@dag(
    dag_id="example_task_sdk_basic",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["task-sdk"],
)
def example_task_sdk_basic():
    """Basic @dag / @task pipeline.""" 

    @task
    def extract() -> int:
        return 42

    @task
    def transform(x: int) -> int:
        return x * 2

    @task
    def load(y: int):
        print("Result:", y)

    load(transform(extract()))


dag = example_task_sdk_basic()
