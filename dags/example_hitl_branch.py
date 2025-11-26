
from __future__ import annotations
from datetime import datetime

from airflow.decorators import dag, task

try:
    from airflow.providers.standard.operators.hitl import HITLBranchOperator  # type: ignore
except Exception:
    HITLBranchOperator = None


@dag(
    dag_id="example_hitl_branch",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["hitl", "branch"],
)
def example_hitl_branch():
    """HITL-like branching example.

    Human chooses which department(s) receive budget.
    Fallback: run all departments.
    """ 

    @task
    def announce_budget():
        return "Choose which departments should receive budget."

    @task
    def allocate_marketing():
        print("📢 Allocating budget to Marketing.")

    @task
    def allocate_rd():
        print("🔬 Allocating budget to R&D.")

    @task
    def allocate_infra():
        print("🏗️ Allocating budget to Infra.")

    start = announce_budget()
    m = allocate_marketing()
    r = allocate_rd()
    i = allocate_infra()

    if HITLBranchOperator:
        branch = HITLBranchOperator(
            task_id="choose_departments",
            subject="Budget allocation decision",
            body="{{ ti.xcom_pull(task_ids='announce_budget') }}",
            options=["Marketing", "R&D", "Infra"],
            options_mapping={
                "Marketing": [m.task_id],
                "R&D": [r.task_id],
                "Infra": [i.task_id],
            },
            multiple=True,
        )
        start >> branch >> [m, r, i]
    else:
        start >> [m, r, i]


dag = example_hitl_branch()
