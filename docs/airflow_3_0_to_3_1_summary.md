# Airflow 3.0 → 3.1 Example Suite

This example suite is intended to:

- Provide small, focused DAGs to test key Airflow concepts.
- Cover Human-in-the-Loop style patterns (simulated using HITL operators or fallbacks),
  deadlines, notifications, and UI features (Gantt, TaskGroup, etc.).
- Serve as a baseline for regression testing when upgrading from Airflow 3.0.x to 3.1.x.

All DAGs are syntactically valid and importable even if some optional providers
(e.g. `apache-airflow-providers-standard` for HITL or `apache-airflow-providers-slack`)
are not installed. In that case, the DAGs fall back to simple dummy behaviour.
