__all__ = ['serialize', 'parse_value', 'parse_literal', 'GraphQLJSON']

from typing import Any, Optional, cast

from graphql import (
    BooleanValueNode,
    FloatValueNode,
    GraphQLScalarType,
    IntValueNode,
    ListValueNode,
    NullValueNode,
    ObjectValueNode,
    StringValueNode,
    ValueNode,
    VariableNode,
)

from graphql_scalars.settings import Settings
from graphql_scalars.types import JsonValueType


def serialize(value: Any) -> JsonValueType:
    value_type = type(value)
    if (json_serializer := Settings.json_serializers.get(value_type)) is None:
        raise TypeError(f'JSON cannot represent {value_type}.')
    else:
        result = json_serializer(value)
        if not isinstance(result, JsonValueType.__args__):  # type: ignore[attr-defined]
            raise TypeError(
                f'JsonSerializer {json_serializer} must return a {JsonValueType} "'
                f'"rather than a {type(result)}'
            )
        return result


def parse_value(value: JsonValueType) -> JsonValueType:
    json_value_types: tuple[type] = JsonValueType.__args__  # type: ignore[attr-defined]
    if not isinstance(value, json_value_types):
        raise TypeError(
            'JSON cannot be represented by non-'
            f'{"/".join(t.__name__ for t in json_value_types)} type'
        )
    # noinspection PyTypeChecker
    return value


def parse_literal(node: ValueNode, variables: Optional[dict[str, Any]] = None) -> Any:
    if node.kind == IntValueNode.kind:
        node = cast(IntValueNode, node)
        return int(node.value)
    elif node.kind == FloatValueNode.kind:
        node = cast(FloatValueNode, node)
        return float(node.value)
    elif node.kind == StringValueNode.kind:
        node = cast(StringValueNode, node)
        return node.value
    elif node.kind == BooleanValueNode.kind:
        node = cast(BooleanValueNode, node)
        return node.value
    elif node.kind == NullValueNode.kind:
        return None
    elif node.kind == VariableNode.kind:
        node = cast(VariableNode, node)
        return variables[node.name.value] if variables is not None else None
    elif node.kind == ListValueNode.kind:
        node = cast(ListValueNode, node)
        return [parse_literal(item, variables) for item in node.values]
    elif node.kind == ObjectValueNode.kind:
        node = cast(ObjectValueNode, node)
        return {field.name.value: parse_literal(field.value, variables) for field in node.fields}


GraphQLJSON = GraphQLScalarType(
    name='JSON',
    description='The `JSON` scalar type represents JSON values as specified by ECMA-404.',
    serialize=serialize,
    parse_value=parse_value,
    parse_literal=parse_literal,
)
