from __future__ import annotations
from datetime import datetime
from airflow.decorators import dag, task

# Semicon simulation scenario (dummy, no real external systems):
# STEP1_CONSUME          : consume Kafka-like message
# STEP2_PARSE            : parse equipment/lot/period/filter
# STEP3_STORE_MSG_DB     : store message meta to PostgreSQL (dummy)
# STEP4_DOWNLOAD         : connect to equipment and download data (dummy)
# STEP5_UPLOAD_S3        : upload data to S3 (dummy)
# STEP6_UPDATE_STATUS_DB : update DB status (dummy)
# STEP7_NOTIFY           : optional notifier
# STEP8_HITL             : optional human approval / branching


import time
from airflow.utils.task_group import TaskGroup

@dag(
    dag_id="example_ui_parallel_gantt",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["semicon", "gantt"],
)
def example_ui_parallel_gantt():
    @task
    def start():
        print("[START] Gantt simulation for semicon equipments")

    @task
    def finish():
        print("[END] Gantt simulation")

    @task
    def simulate(equipment_id: str, duration: int):
        print(f"[STEP4_DOWNLOAD] {equipment_id} long task (sleep={duration})")
        time.sleep(duration)
        print(f"[STEP5_UPLOAD_S3] {equipment_id} upload complete")

    s = start()
    with TaskGroup("heavy") as heavy:
        simulate.override(task_id="tool_a_heavy")("TOOL_A01", 10)
        simulate.override(task_id="tool_b_heavy")("TOOL_B02", 7)
    with TaskGroup("light") as light:
        simulate.override(task_id="tool_c_light")("TOOL_C03", 4)
        simulate.override(task_id="tool_d_light")("TOOL_D04", 2)
    f = finish()
    s >> [heavy, light] >> f

dag = example_ui_parallel_gantt()
