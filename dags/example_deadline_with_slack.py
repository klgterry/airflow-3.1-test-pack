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
    dag_id="example_deadline_with_slack",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["semicon", "deadline", "notifier"],
)
def example_deadline_with_slack():
    @task
    def long_task():
        print("[STEP4_DOWNLOAD] long-running msg processing (sleep 30)")
        time.sleep(30)
        print("[INFO] if exceeded deadline, would send Slack alert (dummy)")

    long_task()

dag = example_deadline_with_slack()
