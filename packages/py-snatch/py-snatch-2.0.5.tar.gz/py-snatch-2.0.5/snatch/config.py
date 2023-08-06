"""Get Environment Secrets for Snatch."""
import os
from typing import Any, Dict

from dotenv import load_dotenv
from loguru import logger
from scalpl import Cut

from snatch.helpers.secrets_manager import SecretManager

load_dotenv()


def get_environment_from_secrets_manager() -> Dict[Any, Any]:
    """Load settings from Secrets Manager..

    :return Dict[Any, Any]
    """
    current_env = os.getenv("ENV", "production")

    secrets = SecretManager(
        current_environment=current_env,
        project_name="snatch",
        current_env_data={},
    )

    secrets_manager_data = {"current_environment": current_env}
    if not secrets.can_read_secrets:
        return secrets_manager_data

    logger.info(
        f"Reading settings from Secrets Manager for "
        f"service: snatch and environment: {current_env} ..."
    )

    secrets_manager_data.update(secrets.get_project_secrets())

    return secrets_manager_data


def get_settings():

    config = {
        "snatch": {
            "boa_vista_secret_token": os.getenv("SNATCH_BOA_VISTA_SECRET_TOKEN", "foo"),
            "datasource_boa_vista_url": os.getenv(
                "SNATCH_DATASOURCE_BOA_VISTA_URL", "http://datasource_boa_vista"
            ),
        }
    }
    config.update(get_environment_from_secrets_manager())

    settings = Cut(config)
    return settings
