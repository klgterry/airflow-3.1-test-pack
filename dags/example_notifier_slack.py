
from __future__ import annotations
from datetime import datetime

from airflow.decorators import dag, task


@dag(
    dag_id="example_notifier_slack",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["notifier", "slack"],
)
def example_notifier_slack():
    """Basic notifier pattern.

    실제 Slack 연동은 Slack webhook / provider 설정 후,
    이 DAG의 실패를 on_failure_callback에 연결해 테스트할 수 있다.
    여기서는 단순히 의도적으로 실패하는 태스크만 제공한다.
    """ 

    @task
    def fail_task():
        raise RuntimeError("Intentional failure for notifier test")

    fail_task()


dag = example_notifier_slack()
