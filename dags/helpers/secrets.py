"""AWS Secrets Manager helper for retrieving pipeline credentials."""

import json
import os
from functools import lru_cache

import boto3


@lru_cache(maxsize=10)
def get_secret(secret_name: str, region: str = None) -> dict:
    """Retrieve and parse a JSON secret from AWS Secrets Manager.

    Results are cached for the lifetime of the process to avoid
    repeated API calls within the same task execution.

    Args:
        secret_name: Name of the secret (e.g., 'banking-pipeline/snowflake')
        region: AWS region (defaults to AWS_DEFAULT_REGION env var)

    Returns:
        Parsed JSON secret as a dict
    """
    region = region or os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
    client = boto3.client("secretsmanager", region_name=region)
    response = client.get_secret_value(SecretId=secret_name)
    return json.loads(response["SecretString"])
