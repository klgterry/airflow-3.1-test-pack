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
    dag_id="example_sla_legacy_simple",
    start_date=datetime(2025, 1, 1),
    schedule="@hourly",
    catchup=False,
    default_args={"sla": timedelta(minutes=10)},
    tags=["semicon", "sla"],
)
def example_sla_legacy_simple():
    @task
    def process_with_sla():
        print("[SLA] must finish msg processing within 10 minutes of schedule")
        time.sleep(2)

    process_with_sla()

@dag(
    dag_id="example_deadline_replacement_simple",
    start_date=datetime(2025, 1, 1),
    schedule="@hourly",
    catchup=False,
    tags=["semicon", "deadline"],
)
def example_deadline_replacement_simple():
    @task
    def process_with_deadline():
        print("[DEADLINE] runtime must not exceed X minutes")
        time.sleep(2)

    process_with_deadline()

sla_dag = example_sla_legacy_simple()
deadline_dag = example_deadline_replacement_simple()
