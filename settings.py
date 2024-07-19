import os
from typing import Any

from dotenv import load_dotenv

from utils.yaml_parser import parse


def get_absolute_yaml_path():
    current_file_path = os.path.abspath(__file__)
    current_dir = os.path.dirname(current_file_path)
    yaml_path = os.path.join(current_dir, "app.yaml")
    return os.path.abspath(yaml_path)


def get_absolute_schema_path():
    current_file_path = os.path.abspath(__file__)
    current_dir = os.path.dirname(current_file_path)
    yaml_path = os.path.join(current_dir, "schema.json")
    return os.path.abspath(yaml_path)


def get_absolute_models_path():
    current_file_path = os.path.abspath(__file__)
    current_dir = os.path.dirname(current_file_path)
    yaml_path = os.path.join(current_dir, "schemas/v1/generated.py")
    return os.path.abspath(yaml_path)


def get_absolute_rest_path():
    current_file_path = os.path.abspath(__file__)
    current_dir = os.path.dirname(current_file_path)
    yaml_path = os.path.join(current_dir, "api/v1/generated.py")
    return os.path.abspath(yaml_path)


def get_absolute_controller_path():
    current_file_path = os.path.abspath(__file__)
    current_dir = os.path.dirname(current_file_path)
    yaml_path = os.path.join(current_dir, "database/controllers/generated.py")
    return os.path.abspath(yaml_path)


YAML_PATH = get_absolute_yaml_path()
SCHEMA_PATH = get_absolute_schema_path()
MODELS_PATH = get_absolute_models_path()
REST_PATH = get_absolute_rest_path()
CONTROLLER_PATH = get_absolute_controller_path()
yaml_data = parse(YAML_PATH)

JSON_SCHEMA_META = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "$schema": {"type": "string"},
        "title": {"type": "string"},
        "type": {"type": "string"},
        "properties": {"type": "object"},
        "required": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["$schema", "title", "type", "properties"],
}


NAME = yaml_data["name"]
HOST = "0.0.0.0"
PORT = 8000

load_dotenv()

DB_DRIVER = "postgresql"
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_URL = os.environ.get("DB_URL")
DB_NAME = os.environ.get("DB_NAME")

ALLOW_ORIGIN = "http://localhost"

DB_FULL_URL = f"{DB_DRIVER}+asyncpg://{DB_USER}:{DB_PASS}@{DB_URL}/{DB_NAME}"

configuration = yaml_data["configuration"]


def update_configuration(key: str, new_data: dict[str, Any]):
    configuration[key] = new_data
