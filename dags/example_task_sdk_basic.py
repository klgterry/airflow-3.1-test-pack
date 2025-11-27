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


@dag(
    dag_id="example_task_sdk_basic",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["semicon", "basic"],
)
def example_task_sdk_basic():
    @task
    def extract() -> dict:
        msg = {
            "msg_id": "kafka-12345",
            "equipment_id": "TOOL_A01",
            "lot_id": "LOT20251126-01",
        }
        print("[STEP1_CONSUME]", msg)
        print("[STEP2_PARSE] parsed equipment/lot from msg")
        return msg

    @task
    def transform(msg: dict) -> dict:
        print(f"[STEP3_STORE_MSG_DB] store msg {msg['msg_id']} into PostgreSQL (dummy)")
        print(f"[STEP4_DOWNLOAD] download data for {msg['equipment_id']} / {msg['lot_id']} (dummy)")
        return msg

    @task
    def load(msg: dict):
        print(f"[STEP5_UPLOAD_S3] upload data for {msg['equipment_id']} to S3 (dummy)")
        print(f"[STEP6_UPDATE_STATUS_DB] mark msg {msg['msg_id']} as SUCCESS")

    load(transform(extract()))

dag = example_task_sdk_basic()
