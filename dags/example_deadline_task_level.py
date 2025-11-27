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

@dag(
    dag_id="example_deadline_task_level",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["semicon", "deadline"],
)
def example_deadline_task_level():
    @task
    def tool_a():
        print("[TOOL_A] STEP4_DOWNLOAD (sleep 5)")
        time.sleep(5)
        print("[TOOL_A] done")

    @task
    def tool_b():
        print("[TOOL_B] STEP4_DOWNLOAD (sleep 15)")
        time.sleep(15)
        print("[TOOL_B] done (might exceed per-task deadline)")

    tool_a() >> tool_b()

dag = example_deadline_task_level()
