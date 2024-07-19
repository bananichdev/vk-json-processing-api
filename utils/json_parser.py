import json

from jsonschema.exceptions import SchemaError, ValidationError
from jsonschema.validators import validate

from settings import JSON_SCHEMA_META, SCHEMA_PATH


def parse_json():
    with open(SCHEMA_PATH) as f:
        schema = json.load(f)
    return validate_json(schema=schema)


def validate_json(schema: dict):
    try:
        validate(instance=schema, schema=JSON_SCHEMA_META)
        return schema
    except ValidationError as e:
        raise ValueError(f"Ошибка валидации JSON схемы: {e.message}") from e
    except SchemaError as e:
        raise ValueError(f"JSON схема некорректна: {e.message}") from e
