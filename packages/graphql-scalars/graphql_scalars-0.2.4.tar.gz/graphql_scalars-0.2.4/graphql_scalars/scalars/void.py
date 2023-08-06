__all__ = ['serialize', 'parse_value', 'parse_literal', 'GraphQLVoid']

from graphql import GraphQLScalarType


def serialize(*_) -> None:
    return None


def parse_value(*_) -> None:
    return None


def parse_literal(*_) -> None:
    return None


GraphQLVoid = GraphQLScalarType(
    name='Void',
    description='A Representation of NULL values',
    serialize=serialize,
    parse_value=parse_value,
    parse_literal=parse_literal,
)
