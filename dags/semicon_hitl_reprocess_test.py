from __future__ import annotations
from datetime import datetime
from airflow.decorators import dag, task
from airflow.providers.standard.operators.hitl import ApprovalOperator


@dag(
    dag_id="semicon_hitl_reprocess_test",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["semicon", "new-feature", "hitl-test"],
)
def semicon_hitl_reprocess_test():
    """HITL 승인 버튼이 실제로 동작하는 테스트 DAG.

    - get_failed_msgs: 재처리 대상 실패 메시지 리스트 조회 (dummy)
    - ApprovalOperator: Airflow UI 에서 Approve / Reject 버튼 노출
        - Approve 선택 시 downstream task 실행
        - Reject 선택 시 downstream task Skip
    - reprocess_msgs: 승인된 경우에만 재처리 로직이 실행된다고 가정
    """

    @task
    def get_failed_msgs() -> list[str]:
        failed = ["msg_101", "msg_102", "msg_103"]
        print("[HITL] failed msgs:", failed)
        return failed

    @task
    def reprocess_msgs(msgs: list[str]):
        print("[HITL] reprocessing msgs (approved):", msgs)
        # 실제 환경에서는 여기서 Kafka 재처리 / FTP 재다운로드 / S3 overwrite 등이 들어갈 자리
        return msgs

    failed = get_failed_msgs()

    # 👇 여기서 실제로 Airflow UI 에 승인 버튼이 생김
    approve_task = ApprovalOperator(
        task_id="approve_reprocess",
        subject="Approve reprocessing of failed semicon messages",
        body=(
            "The following messages failed and are candidates for reprocess:\n\n"
            "{{ ti.xcom_pull(task_ids='get_failed_msgs') }}"
        ),
        defaults="Approve",  # 기본 선택을 Approve 로
    )

    processed = reprocess_msgs(failed)

    # 의존 관계: 실패 메시지 조회 → 승인 → 재처리
    failed >> approve_task >> processed


dag = semicon_hitl_reprocess_test()
