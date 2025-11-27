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
    dag_id="example_asset_with_notifier",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["semicon", "asset", "notifier"],
)
def example_asset_with_notifier():
    @task
    def check() -> bool:
        lot_id = "LOT20251126-01"
        exists = False
        print(f"[CHECK] asset for {lot_id} exists? {exists}")
        return exists

    @task
    def notify():
        print("[STEP7_NOTIFY] asset missing, would notify Slack/webhook (dummy)")

    @task
    def ok():
        print("[OK] asset exists, nothing to do")

    exists = check()
    # simple runtime branch
    if exists:
        ok()
    else:
        notify()

dag = example_asset_with_notifier()
