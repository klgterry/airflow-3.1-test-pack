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
    dag_id="example_schedule_once",
    start_date=datetime(2025, 1, 1),
    schedule="@once",
    catchup=False,
    tags=["semicon", "schedule"],
)
def example_schedule_once():
    @task
    def run_once():
        print("[SCHEDULE] one-off reprocess for specific msg (dummy)")
        time.sleep(1)

    run_once()

@dag(
    dag_id="example_schedule_cron",
    start_date=datetime(2025, 1, 1),
    schedule="0 * * * *",
    catchup=False,
    tags=["semicon", "schedule"],
)
def example_schedule_cron():
    @task
    def run_hourly():
        print("[SCHEDULE] hourly batch that would poll DB for new msgs (dummy)")
        time.sleep(1)

    run_hourly()

once_dag = example_schedule_once()
cron_dag = example_schedule_cron()
