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
    dag_id="example_hitl_entry",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["semicon", "hitl"],
)
def example_hitl_entry():
    @task
    def get_parameters() -> dict:
        params = {
            "equipment_id": "TOOL_A01",
            "lot_id": "LOT20251126-01",
            "from_ts": "2025-11-26T00:00:00Z",
            "to_ts": "2025-11-26T01:00:00Z",
        }
        print("[STEP8_HITL] simulated user input:", params)
        return params

    @task
    def run_with_params(params: dict):
        print("[RUN] reprocess using params (dummy):", params)

    run_with_params(get_parameters())

dag = example_hitl_entry()
