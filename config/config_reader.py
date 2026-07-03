"""
Config reader for the automation framework.

Usage:
    from config.config_reader import get_config
    config = get_config()          # uses ENV var TEST_ENV, defaults to "dev"
    config = get_config("staging") # explicit override

Set the environment via:
    export TEST_ENV=staging   (Mac/Linux)
    $env:TEST_ENV="staging"   (Windows PowerShell)
or pass --env staging if you wire it into pytest via conftest.py (see below).
"""

import os
import yaml
from pathlib import Path

CONFIG_PATH = Path(__file__).parent / "config.yaml"


def get_config(env: str = None) -> dict:
    """
    Load config for the given environment.
    Falls back to TEST_ENV environment variable, then to 'dev'.
    """
    env = env or os.getenv("TEST_ENV", "dev")

    with open(CONFIG_PATH, "r") as f:
        all_configs = yaml.safe_load(f)

    if env not in all_configs:
        raise ValueError(
            f"Environment '{env}' not found in config.yaml. "
            f"Available environments: {list(all_configs.keys())}"
        )

    config = all_configs[env]
    config["env_name"] = env
    return config
