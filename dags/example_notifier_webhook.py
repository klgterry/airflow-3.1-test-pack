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
    dag_id="example_notifier_webhook",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["semicon", "notifier"],
)
def example_notifier_webhook():
    @task
    def summary():
        payload = {
            "processed_msgs": 12,
            "failed_msgs": 1,
            "total_files": 240,
            "total_bytes": 123_456_789,
        }
        print("[SUMMARY]", payload)
        print("[STEP7_NOTIFY] would POST to monitoring webhook (dummy)")

    summary()

dag = example_notifier_webhook()
