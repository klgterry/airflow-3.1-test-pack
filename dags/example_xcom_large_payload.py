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


import json

@dag(
    dag_id="example_xcom_large_payload",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["semicon", "xcom"],
)
def example_xcom_large_payload():
    @task
    def build_files() -> str:
        files = [f"TOOL_A01_LOT20251126_{i:04d}.csv" for i in range(1000)]
        payload = json.dumps({"files": files})
        print("[STEP4_DOWNLOAD] built list of", len(files), "files")
        return payload

    @task
    def consume_files(payload: str):
        data = json.loads(payload)
        files = data["files"]
        print("[STEP5_UPLOAD_S3] would upload", len(files), "files (dummy)")
        print(" first 3:", files[:3])

    consume_files(build_files())

dag = example_xcom_large_payload()
