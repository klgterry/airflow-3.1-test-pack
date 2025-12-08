from __future__ import annotations
from datetime import datetime
import time
import random
from airflow.decorators import dag, task

DEADLINE_SECONDS = 30


@dag(
    dag_id="semicon_deadline_guard_test",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["semicon", "new-feature", "deadline-test"],
)
def semicon_deadline_guard_test():
    """Deadline 기능 강화 테스트 DAG.

    - 여러 장비를 (사실상) 병렬로 처리한다고 가정
    - 전체 실행 시간이 DEADLINE_SECONDS 를 넘으면 RuntimeError 로 FAIL
    """

    @task
    def start_timer() -> float:
        start = time.time()
        print(f"[DEADLINE_TEST] start_ts={start}")
        return start

    @task
    def process_equipment(equipment_id: str) -> float:
        duration = random.randint(5, 15)
        print(f"[STEP4_DOWNLOAD] {equipment_id} downloading... (sleep={duration})")
        time.sleep(duration)
        print(f"[STEP5_UPLOAD_S3] {equipment_id} upload done (dummy)")
        return float(duration)

    @task
    def check_deadline(start_ts: float, durations: list[float]):
        end_ts = time.time()
        total_runtime = end_ts - start_ts
        print(f"[DEADLINE_TEST] durations={durations}, total_runtime={total_runtime:.2f}s")

        if total_runtime > DEADLINE_SECONDS:
            raise RuntimeError(
                f"[DEADLINE_TEST] total_runtime {total_runtime:.2f}s "
                f"> DEADLINE_SECONDS({DEADLINE_SECONDS})"
            )
        print("[DEADLINE_TEST] within deadline, PASS")

    start_ts = start_timer()
    d1 = process_equipment.override(task_id="tool_a")("TOOL_A01")
    d2 = process_equipment.override(task_id="tool_b")("TOOL_B02")
    d3 = process_equipment.override(task_id="tool_c")("TOOL_C03")
    check_deadline(start_ts, [d1, d2, d3])


dag = semicon_deadline_guard_test()
