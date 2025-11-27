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
    dag_id="example_hitl_approval",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["semicon", "hitl"],
)
def example_hitl_approval():
    @task
    def request_approval() -> str:
        print("[STEP8_HITL] request approval to reprocess msg (dummy)")
        return "approved"  # simulate always approved

    @task
    def reprocess():
        print("[HITL] approved -> reprocess Kafka msg and overwrite S3 data (dummy)")

    decision = request_approval()
    reprocess(decision)

dag = example_hitl_approval()
