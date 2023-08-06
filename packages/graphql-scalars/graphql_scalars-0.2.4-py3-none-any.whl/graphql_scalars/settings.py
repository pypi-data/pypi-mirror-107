__all__ = ['Settings']

from typing import Any, Callable, ClassVar

from graphql_scalars.types import JsonValueType


def json_value_serializer(v):
    return v


class Settings:
    json_serializers: ClassVar[dict[type, Callable[[Any], JsonValueType]]] = {
        t: json_value_serializer for t in JsonValueType.__args__  # type: ignore[attr-defined]
    }


has_tried_to_import_pydantic: bool = False

if not has_tried_to_import_pydantic:
    try:
        from pydantic import BaseModel

        def convert_pydantic_to_dict(m: BaseModel) -> dict:
            return m.dict()

        Settings.json_serializers[BaseModel] = convert_pydantic_to_dict

    except ImportError:
        pass

    has_tried_to_import_pydantic = True
