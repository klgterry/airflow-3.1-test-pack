from __future__ import annotations
from datetime import datetime
from airflow.decorators import dag, task

@dag(
    dag_id="semicon_hitl_reprocess_test",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["semicon", "new-feature", "hitl-test"],
)
def semicon_hitl_reprocess_test():

    @task
    def get_failed_msgs():
        failed = ["msg_101", "msg_102", "msg_103"]
        print("[HITL] failed msgs:", failed)
        return failed

    @task
    def get_approvals(failed_msgs: list[str]):
        approved = failed_msgs[:2]
        print("[HITL] approved msgs:", approved)
        return approved

    @task
    def reprocess_msgs(msgs: list[str]):
        print("[HITL] reprocessing msgs:", msgs)
        return msgs

    @task
    def validate(failed: list[str], approved: list[str], processed: list[str]):
        if set(approved) != set(processed):
            raise RuntimeError("[HITL] processed != approved")
        print("[HITL] PASS: processed matches approved")

    failed = get_failed_msgs()
    approved = get_approvals(failed)
    processed = reprocess_msgs(approved)
    validate(failed, approved, processed)

dag = semicon_hitl_reprocess_test()
