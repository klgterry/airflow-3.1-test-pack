# Airflow 3.1 Test Full Package

This repository contains an example pack for testing Apache Airflow 3.1.x features:

- Human-in-the-Loop style flows (simulated via HITL operators or fallbacks)
- Long-running DAGs for deadline-style behaviour
- Notifier patterns (Slack-ready)
- Task SDK (@dag, @task) examples
- TaskGroup / deferrable HTTP sensor / Gantt UI behaviour

## How to run (local Docker Compose)

```bash
cd docker
docker build -t airflow-3-1-test:3.1.2 -f Dockerfile_3.1.2 ..
docker compose run --rm airflow-init
docker compose up -d
```

Then open:

- http://localhost:8080
- ID: admin
- PW: admin

Enable the DAGs in the UI and trigger runs.
