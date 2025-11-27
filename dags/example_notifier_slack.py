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


import random

@dag(
    dag_id="example_notifier_slack",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["semicon", "notifier"],
)
def example_notifier_slack():
    @task
    def download():
        msg_id = "kafka-err-001"
        equipment_id = "TOOL_A01"
        r = random.random()
        print(f"[STEP4_DOWNLOAD] equipment={equipment_id}, random={r}")
        if r < 0.7:
            print("[ERROR] download failed, would trigger Slack in real env")
            raise RuntimeError("Simulated download failure")
        print("[OK] download succeeded")

    download()

dag = example_notifier_slack()
