from fastapi import APIRouter, Query
from utils.config_loader import DEFAULTS,load_yaml,load_cli_overrides,load_os_env,load_dotenv_config

router = APIRouter()


@router.get("/effective-config")
def effective_config(
    set: list[str] = Query(default=[])
):
    config = DEFAULTS.copy()

    config.update(load_yaml())

    config.update(load_dotenv_config())

    config.update(load_os_env())

    config.update(load_cli_overrides(set))

    config["api_key"] = "****"

    return config