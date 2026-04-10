# Airflow Orchestrator

Standalone Airflow instance that orchestrates multiple data pipeline projects.

## Architecture

```
EC2 (t4g.small)
├── /home/ubuntu/airflow-orchestrator/        ← this repo (Airflow infra)
├── /home/ubuntu/iot-fleet-monitor-pipeline/  ← project 1 (git repo)
└── /home/ubuntu/banking-data-vault-pipeline/ ← project 2 (git repo)
```

Airflow mounts DAG files and dbt projects from each project repo via Docker volumes.
Each project owns its DAG code — Airflow only contains shared infrastructure.

## Setup

1. Clone this repo and all project repos on EC2
2. Copy `.env.example` to `.env` and fill in credentials
3. Copy Snowflake private key to `keys/snowflake_key.p8`
4. `docker compose up -d --build`

## Adding a new project

1. Clone the project repo on EC2
2. Add volume mounts to `docker-compose.yml` (DAG file + dbt project)
3. `docker compose restart`

## Deploying updates

```bash
cd /home/ubuntu/<project-repo> && git pull
# Airflow auto-detects changes within 2 minutes
```
