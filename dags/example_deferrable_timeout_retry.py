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


from datetime import timedelta
import time

@dag(
    dag_id="example_deferrable_timeout_retry",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    default_args={"retries": 1, "retry_delay": timedelta(seconds=10)},
    tags=["semicon", "timeout"],
)
def example_deferrable_timeout_retry():
    @task
    def slow_download():
        print("[STEP4_DOWNLOAD] slow download simulation (sleep 10)")
        time.sleep(10)
        print("[DONE] slow download finished")

    slow_download()

dag = example_deferrable_timeout_retry()
