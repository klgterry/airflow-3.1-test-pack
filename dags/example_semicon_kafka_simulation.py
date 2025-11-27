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


from typing import Dict, Any, List

@dag(
    dag_id="example_semicon_kafka_simulation",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["semicon", "full"],
)
def example_semicon_kafka_simulation():
    @task
    def consume_kafka() -> Dict[str, Any]:
        msg = {
            "msg_id": "kafka-12345",
            "equipment_id": "TOOL_A01",
            "lot_id": "LOT20251126-01",
            "from_ts": "2025-11-26T00:00:00Z",
            "to_ts": "2025-11-26T01:00:00Z",
        }
        print("[STEP1_CONSUME]", msg)
        print("[STEP2_PARSE] parsed semicon fields")
        return msg

    @task
    def store_msg(msg: Dict[str, Any]) -> int:
        print(f"[STEP3_STORE_MSG_DB] insert msg {msg['msg_id']} into PostgreSQL (dummy)")
        return 1001

    @task
    def download_data(msg: Dict[str, Any]) -> List[str]:
        paths = [
            f"/tmp/semicon/{msg['equipment_id']}_{msg['lot_id']}_part1.csv",
            f"/tmp/semicon/{msg['equipment_id']}_{msg['lot_id']}_part2.csv",
        ]
        print("[STEP4_DOWNLOAD] simulate download:", paths)
        return paths

    @task
    def upload_s3(paths: List[str], msg: Dict[str, Any]) -> List[str]:
        keys = []
        for p in paths:
            fname = p.split("/")[-1]
            key = f"semicon/{msg['equipment_id']}/{msg['lot_id']}/{fname}"
            print(f"[STEP5_UPLOAD_S3] {p} -> s3://my-bucket/{key} (dummy)")
            keys.append(key)
        return keys

    @task
    def update_status(message_pk: int, s3_keys: List[str]):
        status = "SUCCESS" if s3_keys else "NO_DATA"
        print(f"[STEP6_UPDATE_STATUS_DB] pk={message_pk}, status={status}, keys={s3_keys}")

    msg = consume_kafka()
    pk = store_msg(msg)
    paths = download_data(msg)
    keys = upload_s3(paths, msg)
    update_status(pk, keys)

dag = example_semicon_kafka_simulation()
