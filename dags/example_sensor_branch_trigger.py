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


from airflow.operators.python import BranchPythonOperator

ALLOWED_EQUIPMENTS = ["TOOL_A01", "TOOL_B02"]

@dag(
    dag_id="example_sensor_branch_trigger",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["semicon", "branch"],
)
def example_sensor_branch_trigger():
    @task
    def consume() -> dict:
        msg = {"msg_id": "kafka-99999", "equipment_id": "TOOL_X99", "lot_id": "LOT_TEST"}
        print("[STEP1_CONSUME]", msg)
        return msg

    def _choose(equipment_id: str, **_):
        if equipment_id in ALLOWED_EQUIPMENTS:
            print(f"[BRANCH] {equipment_id} allowed -> process")
            return "process"
        print(f"[BRANCH] {equipment_id} NOT allowed -> skip")
        return "skip"

    branch = BranchPythonOperator(
        task_id="branch_on_equipment",
        python_callable=_choose,
        op_kwargs={"equipment_id": "{{ ti.xcom_pull(task_ids='consume')['equipment_id'] }}"},
    )

    @task
    def process(msg: dict):
        print(f"[STEP3_STORE_MSG_DB] allowed msg {msg['msg_id']} (dummy)")
        print(f"[STEP4_DOWNLOAD] for {msg['equipment_id']} (dummy)")
        print("[STEP5_UPLOAD_S3] upload (dummy)")

    @task
    def skip(msg: dict):
        print(f"[STEP3_STORE_MSG_DB] mark msg {msg['msg_id']} as SKIPPED (dummy)")

    m = consume()
    m >> branch
    branch >> [process(m), skip(m)]

dag = example_sensor_branch_trigger()
