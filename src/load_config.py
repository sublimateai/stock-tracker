from pathlib import Path
from typing import Any
import yaml


def load_client_config() -> dict[str, Any]:
    with open(Path(__file__).parent.parent / "configs" / "client.yml") as f:
        return yaml.safe_load(f)


def load_server_config() -> dict[str, Any]:
    with open(Path(__file__).parent.parent / "configs" / "server.yml") as f:
        return yaml.safe_load(f)
