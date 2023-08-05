"""Get Environment Secrets for Snatch."""
from typing import Any, Dict

from loguru import logger
from stela import StelaOptions
from stela.decorators import post_load

from snatch.helpers.secrets_manager import SecretManager


@post_load
def get_environment_from_secrets_manager(
    data: dict, options: StelaOptions, force_read: bool = False
) -> Dict[Any, Any]:
    """Load settings from Secrets Manager to current Stela data.

    Data returned must be a Python Dictionary.

    :param force_read: Force Read from Secrets Manager
    :param data: (dict) Data parsed from previous phases
    :param options: (StelaOptions) Stela Options from pyproject.toml configuration
    :return Dict[Any, Any]
    """
    environment = options.current_environment

    secrets = SecretManager(
        current_environment=environment,
        project_name="snatch",
        current_env_data=data,
    )

    if not secrets.can_read_secrets and not force_read:
        return data

    logger.info(
        f"Reading settings from Secrets Manager for "
        f"service: snatch and environment: {environment} ..."
    )

    secrets_manager_data = secrets.get_project_secrets()

    return secrets_manager_data
