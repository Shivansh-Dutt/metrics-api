import yaml

from dotenv import dotenv_values

import os

DEFAULTS = {
    "port": 8000,
    "workers": 1,
    "debug": False,
    "log_level": "info",
    "api_key": "default-secret-000",
}

def load_yaml():

    with open("config.development.yaml") as f:

        return yaml.safe_load(f)

def load_dotenv_config():

    env = dotenv_values("metrics-api\\.env")
    
    config = {}

    if "APP_PORT" in env:
        config["port"] = int(env["APP_PORT"])

    if "NUM_WORKERS" in env:
        config["workers"] = int(env["NUM_WORKERS"])
        
    if "APP_LOG_LEVEL" in env:
        config["log_level"] = env["APP_LOG_LEVEL"]

    return config

def to_bool(value: str):
    return value.lower() in {"true", "1", "yes", "on"}


def load_os_env():

    config = {}

    if "APP_PORT" in os.environ:
        config["port"] = int(os.environ["APP_PORT"])

    if "APP_WORKERS" in os.environ:
        config["workers"] = int(os.environ["APP_WORKERS"])

    if "APP_DEBUG" in os.environ:
        config["debug"] = to_bool(os.environ["APP_DEBUG"])

    if "APP_LOG_LEVEL" in os.environ:
        config["log_level"] = os.environ["APP_LOG_LEVEL"]

    if "APP_API_KEY" in os.environ:
        config["api_key"] = os.environ["APP_API_KEY"]

    return config

def load_cli_overrides(values: list[str]):

    config = {}

    for item in values:

        key, value = item.split("=", 1)

        if key in {"port", "workers"}:
            config[key] = int(value)

        elif key == "debug":
            config[key] = to_bool(value)

        else:
            config[key] = value

    return config