from typing import Any

from settings import MODELS_PATH
from utils.json_parser import parse_json

nested_models = []


def parse_property(prop: str, details: dict[str, Any], required: bool) -> str:
    prop_type = details.get("type")
    optional = not required

    type_annotation = "Any"

    if prop_type == "string":
        if details.get("format") == "date-time":
            type_annotation = "Optional[datetime]" if optional else "datetime"
        elif details.get("format") == "uri":
            type_annotation = "Optional[AnyUrl]" if optional else "AnyUrl"
        else:
            type_annotation = "Optional[str]" if optional else "str"
    elif prop_type == "integer":
        type_annotation = "Optional[int]" if optional else "int"
    elif prop_type == "number":
        type_annotation = "Optional[float]" if optional else "float"
    elif prop_type == "boolean":
        type_annotation = "Optional[bool]" if optional else "bool"
    elif prop_type == "array":
        items = details.get("items", {})
        item_type = parse_property("item", items, True).split(": ")[1]
        type_annotation = f"Optional[list[{item_type}]]" if optional else f"list[{item_type}]"
    elif prop_type == "object":
        nested_model_name = prop.capitalize()
        nested_model_code = json_schema_to_pydantic_model(details, nested_model_name)
        nested_models.append(nested_model_code)
        type_annotation = f"Optional[{nested_model_name}]" if optional else nested_model_name

    return f"\t{prop}: {type_annotation}"


def json_schema_to_pydantic_model(schema: dict[str, Any], model_name: str) -> str:
    properties = schema.get("properties", {})
    required = schema.get("required", [])

    class_definitions = []

    for prop, details in properties.items():
        class_definitions.append(parse_property(prop, details, prop in required))

    class_code = f"class {model_name}(BaseModel):\n"
    class_code += "\n".join(class_definitions) + "\n"

    return class_code


def main():
    schema = parse_json()

    model_name = schema.get("title", "GeneratedModel")
    model_code = json_schema_to_pydantic_model(schema, model_name)

    print(f"Генерация моделей в {MODELS_PATH} ...")
    with open(MODELS_PATH, "w") as f:
        f.write("from pydantic import BaseModel, AnyUrl\n")
        f.write("from typing import Optional\n")
        f.write("from datetime import datetime\n\n\n")
        f.write(model_code)
        for nested_model in nested_models:
            f.write(nested_model)
            f.write("\n")
    print("Генерация прошла успешно!")


if __name__ == "__main__":
    main()
