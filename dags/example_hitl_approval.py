
from __future__ import annotations
from datetime import datetime

from airflow.decorators import dag, task
from airflow.operators.python import BranchPythonOperator

try:
    from airflow.providers.standard.operators.hitl import ApprovalOperator  # type: ignore
except Exception:  # provider not installed
    ApprovalOperator = None


@dag(
    dag_id="example_hitl_approval",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["hitl", "approval"],
)
def example_hitl_approval():
    """HITL Approval-style example.

    If HITL provider is not installed, falls back to a dummy approval step.
    """ 

    @task
    def generate_message() -> str:
        return "Review this pipeline change and decide whether to proceed."

    def _branch(**context) -> str:
        result = context["ti"].xcom_pull(task_ids="wait_for_approval")
        if isinstance(result, dict):
            status = result.get("status") or result.get("result") or result.get("choice")
        else:
            status = result
        if str(status).lower().startswith("approve"):
            return "after_approved"
        return "after_rejected"

    branch = BranchPythonOperator(
        task_id="branch_on_approval",
        python_callable=_branch,
    )

    @task(task_id="after_approved")
    def after_approved():
        print("✅ Human APPROVED. Proceeding with rollout.")

    @task(task_id="after_rejected")
    def after_rejected():
        print("❌ Human REJECTED. Aborting or rolling back.")

    msg = generate_message()

    if ApprovalOperator:
        approval = ApprovalOperator(
            task_id="wait_for_approval",
            subject="Approval required: Pipeline change",
            body="{{ ti.xcom_pull(task_ids='generate_message') }}",
        )
        msg >> approval >> branch
    else:
        @task(task_id="wait_for_approval")
        def fake_approval():
            print("ApprovalOperator not available, simulating 'approved'.")
            return "approved"
        fake = fake_approval()
        msg >> fake >> branch

    branch >> [after_approved(), after_rejected()]


dag = example_hitl_approval()
