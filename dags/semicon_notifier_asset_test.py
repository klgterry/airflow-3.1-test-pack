from __future__ import annotations
from datetime import datetime
from airflow.decorators import dag, task


@dag(
    dag_id="semicon_notifier_asset_test",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["semicon", "new-feature", "notifier-asset-test"],
)
def semicon_notifier_asset_test():
    """Asset + Notifier 신규 기능 테스트 DAG.

    - expected_lots: 오늘 처리해야 할 LOT 목록 (기대값)
    - existing_assets: 실제로 존재하는 LOT asset 목록 (dummy)
    - check_missing: 누락된 LOT 계산
    - notify_if_needed: 누락된 LOT 가 있으면 Slack/Webhook 으로 알림 보낸다고 가정
    - validate: expected = existing + missing 구조 검증, 어긋나면 FAIL
    """

    @task
    def expected_lots():
        lots = ["LOT_A", "LOT_B", "LOT_C"]
        print("[ASSET] expected lots:", lots)
        return lots

    @task
    def existing_assets():
        existing = ["LOT_A", "LOT_C"]
        print("[ASSET] existing assets:", existing)
        return existing

    @task
    def check_missing(expected: list[str], existing: list[str]):
        missing = sorted(set(expected) - set(existing))
        print("[ASSET] missing:", missing)
        return missing

    @task
    def notify_if_needed(missing: list[str]):
        if missing:
            print(f"[NOTIFY] missing lots: {missing}, would send Slack/Webhook")
        else:
            print("[NOTIFY] all lots present")

    @task
    def validate(expected: list[str], existing: list[str], missing: list[str]):
        if len(expected) == len(existing) + len(missing):
            print("[ASSET] PASS structure validated")
        else:
            raise RuntimeError("[ASSET] structure mismatch!")

    exp = expected_lots()
    exi = existing_assets()
    miss = check_missing(exp, exi)
    notify_if_needed(miss)
    validate(exp, exi, miss)


dag = semicon_notifier_asset_test()
