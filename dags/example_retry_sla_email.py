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
import random

@dag(
    dag_id="example_retry_sla_email",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    default_args={"retries": 2, "retry_delay": timedelta(seconds=5), "sla": timedelta(minutes=5)},
    tags=["semicon", "retry"],
)
def example_retry_sla_email():
    @task
    def unstable_download():
        r = random.random()
        print("[STEP4_DOWNLOAD] unstable network, random=", r)
        if r < 0.7:
            print("[WARN] download error, will retry within SLA window")
            raise RuntimeError("Simulated transient failure")
        print("[OK] download succeeded")

    unstable_download()

dag = example_retry_sla_email()
