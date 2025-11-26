
from __future__ import annotations
from datetime import datetime
import time

from airflow.decorators import dag, task
from airflow.utils.task_group import TaskGroup


@dag(
    dag_id="example_task_group_parallel",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["taskgroup"],
)
def example_task_group_parallel():
    """TaskGroup-based parallel work example.""" 

    @task
    def start():
        print("Start")

    @task
    def end():
        print("End")

    @task
    def work(i: int):
        time.sleep(1)
        print("Work", i)

    s = start()
    with TaskGroup("parallel_group") as group:
        for i in range(5):
            work.override(task_id=f"work_{i}")(i)
    e = end()

    s >> group >> e


dag = example_task_group_parallel()
