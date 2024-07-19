import re
from typing import Any

import yaml


def parse(file_path: str) -> dict[str, Any]:
    with open(file_path, "r") as file:
        try:
            data = yaml.safe_load(file)
            return validate(data)
        except yaml.YAMLError as exc:
            raise ValueError(f"Error parsing YAML file: {exc}") from exc


def validate(data: dict[str, Any]) -> dict[str, Any]:
    if "kind" not in data:
        raise ValueError('Missing "kind" in yaml file')
    if "name" not in data:
        raise ValueError('Missing "name" in yaml file')
    if "description" not in data:
        raise ValueError('Missing "description" in yaml file')
    if "version" not in data:
        raise ValueError('Missing "version" in yaml file')
    if not re.match(
        r"^\d+\.\d+\.\d+$",
        data["version"],
    ):
        raise ValueError("Invalid version format. It should be in MAJOR.MINOR.PATCH format.")
    if "configuration" not in data:
        raise ValueError('Missing "configuration" in yaml file')
    if "specification" not in data["configuration"]:
        raise ValueError('Missing "specification" in yaml file (configuration block)')
    if "settings" not in data["configuration"]:
        raise ValueError('Missing "settings" in yaml file (configuration block)')
    return data
