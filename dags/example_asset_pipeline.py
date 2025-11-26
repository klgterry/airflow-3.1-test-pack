
from __future__ import annotations
from datetime import datetime

from airflow.decorators import dag, task


@dag(
    dag_id="example_asset_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["asset"],
)
def example_asset_pipeline():
    """Simple asset-like pipeline: produce → consume.""" 

    @task
    def produce_asset() -> str:
        return "asset_v1"

    @task
    def consume_asset(a: str):
        print("Consuming asset:", a)

    consume_asset(produce_asset())


dag = example_asset_pipeline()
