# Airflow Orchestrator

Standalone Airflow instance that orchestrates multiple data pipeline projects.

## Architecture

```
EC2 (t4g.small)
├── /home/ubuntu/airflow-orchestrator/        ← this repo (Airflow infra)
├── /home/ubuntu/banking-data-vault-pipeline/ ← project 1 (git repo)
└── /home/ubuntu/<future-project>/            ← project N (git repo)
```

Airflow mounts DAG files and dbt projects from each project repo via Docker volumes.
Each project owns its DAG code — Airflow only contains shared infrastructure.

## Credentials

All pipeline credentials are stored in **AWS Secrets Manager** — not in .env files.
The only credentials in `.env` are AWS access keys (needed to reach Secrets Manager).

Secrets used:
- `banking-pipeline/snowflake` — Snowflake account, user, role, warehouse, database
- `banking-pipeline/s3-config` — S3 bucket configuration

DAGs call `helpers.secrets.get_secret("banking-pipeline/snowflake")` at runtime.

## Setup

1. Clone this repo and all project repos on EC2
2. Copy `.env.example` to `.env` and fill in AWS credentials
3. Copy Snowflake private key to `keys/snowflake_key.p8`
4. `docker compose up -d --build`

## Adding a new project

1. Clone the project repo on EC2
2. Add volume mounts to `docker-compose.yml`:
   - DAG file: `/home/ubuntu/<project>/airflow/dags/<dag>.py:/opt/airflow/dags/<dag>.py`
   - dbt project: `/home/ubuntu/<project>/dbt/<name>:/opt/airflow/dbt/<name>`
3. Add project secrets to AWS Secrets Manager
4. `docker compose restart`

## Deploying updates

```bash
cd /home/ubuntu/<project-repo> && git pull
# Airflow auto-detects DAG changes within 2 minutes
```
