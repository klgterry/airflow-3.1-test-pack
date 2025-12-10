import random
import time
from datetime import datetime, timedelta

from airflow.decorators import dag, task
from airflow.utils.task_group import TaskGroup
from airflow.operators.empty import EmptyOperator

EQUIPMENTS_HEAVY = [f"EQ_{i:02d}" for i in range(1, 33)]

default_args = {
    "owner": "airflow",
    "retries": 1,
    "retry_delay": timedelta(seconds=10),
}

@task
def prepare_lot():
    print("[LOAD_TEST] preparing lot for heavy parallel test")
    return {"lot_id": "LOT_HEAVY_TEST"}

@task
def process_equipment(equipment_id: str, lot_info: dict):
    duration = random.randint(10, 20)
    print(f"[LOAD_TEST] {equipment_id} processing lot {lot_info['lot_id']} for {duration}s")
    time.sleep(duration)
    print(f"[LOAD_TEST] {equipment_id} done")
    return {"equipment_id": equipment_id, "lot_id": lot_info["lot_id"], "duration": duration}

@task
def summarize(results: list):
    total = len(results)
    avg_duration = sum(r["duration"] for r in results) / total
    print(f"[LOAD_TEST] processed {total} equipments, avg_duration={avg_duration:.1f}s")
    return {"total": total, "avg_duration": avg_duration}

@dag(
    dag_id="example_task_group_parallel_heavy",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    default_args=default_args,
    tags=["semicon", "load_test", "parallel"],
)
def example_task_group_parallel_heavy():
    start = EmptyOperator(task_id="start")
    end = EmptyOperator(task_id="end")

    lot_info = prepare_lot()

    with TaskGroup(group_id="process_all_equipments") as tg:
        results = []
        for eq in EQUIPMENTS_HEAVY:
            t = process_equipment.override(task_id=f"process_{eq}")(eq, lot_info)
            results.append(t)

    summary = summarize(results)

    start >> lot_info >> tg >> summary >> end

dag = example_task_group_parallel_heavy()