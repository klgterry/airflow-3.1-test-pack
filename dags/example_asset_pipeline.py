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
    dag_id="example_asset_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["semicon", "asset"],
)
def example_asset_pipeline():
    @task
    def produce() -> dict:
        asset = {
            "lot_id": "LOT20251126-01",
            "equipment_ids": ["TOOL_A01", "TOOL_B02"],
            "s3_base": "semicon/LOT20251126-01/",
        }
        print("[ASSET] produced:", asset)
        return asset

    @task
    def consume(asset: dict):
        print("[ASSET] consumed for reporting (dummy):", asset)

    consume(produce())

dag = example_asset_pipeline()
