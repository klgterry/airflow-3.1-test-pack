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
    dag_id="example_hitl_required_actions_view",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["semicon", "hitl"],
)
def example_hitl_required_actions_view():
    @task
    def list_pending():
        pending = [
            {"msg_id": "kafka-2001", "equipment_id": "TOOL_A01"},
            {"msg_id": "kafka-2002", "equipment_id": "TOOL_B02"},
        ]
        print("[HITL_VIEW] pending approvals:", pending)

    list_pending()

dag = example_hitl_required_actions_view()
