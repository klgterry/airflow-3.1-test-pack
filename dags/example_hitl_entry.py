
from __future__ import annotations
from datetime import datetime

from airflow.decorators import dag, task
from airflow.models.param import Param

try:
    from airflow.providers.standard.operators.hitl import HITLEntryOperator  # type: ignore
except Exception:
    HITLEntryOperator = None


@dag(
    dag_id="example_hitl_entry",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    params={
        "default_priority": Param("medium", enum=["low", "medium", "high"]),
    },
    tags=["hitl", "entry"],
)
def example_hitl_entry():
    """HITL-like form entry example.

    If HITLEntryOperator is unavailable, falls back to a simple dummy task.
    """ 

    @task
    def prepare_question() -> str:
        return "How should we prioritize this feature request?"

    question = prepare_question()

    if HITLEntryOperator:
        entry = HITLEntryOperator(
            task_id="wait_for_input",
            subject="Feature prioritization input",
            body="{{ ti.xcom_pull(task_ids='prepare_question') }}",
            params={
                "priority": Param("medium", enum=["low", "medium", "high"]),
                "comment": Param("", description="Why this priority?"),
            },
        )

        @task
        def consume_input(params_input: dict):
            print("📥 Received HITL input:", params_input)

        consume_input(entry.output.get("params_input"))
    else:
        @task
        def fallback():
            print("HITLEntryOperator not available. Using fallback.")
        question >> fallback()


dag = example_hitl_entry()
