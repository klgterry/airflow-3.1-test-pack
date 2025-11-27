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
    dag_id="example_hitl_multi_approver",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["semicon", "hitl"],
)
def example_hitl_multi_approver():
    @task
    def op_approval() -> bool:
        print("[HITL] operations approves global reprocess (dummy)")
        return True

    @task
    def qa_approval() -> bool:
        print("[HITL] QA approves global reprocess (dummy)")
        return True

    @task
    def execute(op_ok: bool, qa_ok: bool):
        if op_ok and qa_ok:
            print("[EXEC] all approvers OK -> run global reprocess (dummy)")
        else:
            print("[EXEC] approval denied")

    execute(op_approval(), qa_approval())

dag = example_hitl_multi_approver()
