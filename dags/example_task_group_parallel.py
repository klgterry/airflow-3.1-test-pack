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

EQUIPMENTS = ["TOOL_A01", "TOOL_B02", "TOOL_C03", "TOOL_D04", "TOOL_E05"]

@dag(
    dag_id="example_task_group_parallel",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["semicon", "taskgroup"],
)
def example_task_group_parallel():
    @task
    def start():
        print("[START] Semicon multi-equipment processing")

    @task
    def end():
        print("[END] Semicon multi-equipment processing")

    @task
    def process_equipment(equipment_id: str):
        print(f"[STEP4_DOWNLOAD] downloading from {equipment_id} (dummy)")
        time.sleep(1)
        print(f"[STEP5_UPLOAD_S3] uploading {equipment_id} data to S3 (dummy)")

    s = start()
    with TaskGroup("equipments") as grp:
        for eq in EQUIPMENTS:
            process_equipment.override(task_id=f"process_{eq.lower()}")(eq)
    e = end()
    s >> grp >> e

dag = example_task_group_parallel()
