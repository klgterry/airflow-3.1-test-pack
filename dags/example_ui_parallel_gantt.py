
from __future__ import annotations
from datetime import datetime
import time

from airflow.decorators import dag, task
from airflow.utils.task_group import TaskGroup


@dag(
    dag_id="example_ui_parallel_gantt",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["ui", "gantt"],
)
def example_ui_parallel_gantt():
    """DAG designed to show a clear Gantt chart with parallel tasks.""" 

    @task
    def start():
        print("Starting DAG")

    @task
    def finish():
        print("Finishing DAG")

    @task
    def sleep_task(duration: int):
        print(f"Sleeping for {duration} seconds...")
        time.sleep(duration)

    s = start()

    with TaskGroup("group_long") as group_long:
        sleep_task.override(task_id="long_3s")(3)
        sleep_task.override(task_id="long_7s")(7)
        sleep_task.override(task_id="long_10s")(10)

    with TaskGroup("group_short") as group_short:
        sleep_task.override(task_id="short_2s")(2)
        sleep_task.override(task_id="short_5s")(5)

    f = finish()

    s >> [group_long, group_short] >> f


dag = example_ui_parallel_gantt()
