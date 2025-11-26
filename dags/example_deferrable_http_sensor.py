
from __future__ import annotations
from datetime import datetime

from airflow.decorators import dag, task

try:
    from airflow.providers.http.sensors.http import HttpSensorAsync  # type: ignore
except Exception:
    HttpSensorAsync = None


@dag(
    dag_id="example_deferrable_http_sensor",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["deferrable", "http"],
)
def example_deferrable_http_sensor():
    """Deferrable HTTP sensor example.

    If HttpSensorAsync is not available, we fallback to a simple dummy task.
    """ 

    @task
    def after_sensor():
        print("HTTP condition satisfied (or simulated).")

    if HttpSensorAsync:
        sensor = HttpSensorAsync(
            task_id="wait_http",
            http_conn_id="http_default",
            endpoint="",  # configure as needed
        )
        sensor >> after_sensor()
    else:
        after_sensor()


dag = example_deferrable_http_sensor()
