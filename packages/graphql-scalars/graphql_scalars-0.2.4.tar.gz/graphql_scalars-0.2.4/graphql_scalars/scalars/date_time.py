__all__ = ['serialize', 'parse_value', 'GraphQLDateTime']

from datetime import date, datetime, timezone
from typing import Union

import arrow
from arrow import Arrow
from graphql import GraphQLScalarType


def serialize(value: Union[datetime, date, Arrow, str]) -> str:
    if not isinstance(value, (datetime, date, Arrow, str)):
        raise TypeError('DateTime cannot represent non-datetime/date/Arrow/str type')
    dt = arrow.get(value).astimezone(timezone.utc)
    return dt.isoformat()


def parse_value(value: str) -> datetime:
    if not isinstance(value, str):
        raise TypeError('DateTime cannot be represented by non-str type')
    dt = arrow.get(value)
    # A datetime string without timezone is not allowed!
    # A datetime string must be separated by 'T'.
    # A timezone mark is one of ['+', '-', 'Z'].
    if (sep_index := value.find('T')) != -1 and not {'+', '-', 'Z'}.intersection(value[sep_index:]):
        raise ValueError('DateTime cannot be represented by a no-timezone format')
    return dt.astimezone(timezone.utc)


GraphQLDateTime = GraphQLScalarType(
    name='DateTime',
    description=(
        'A date-time string at UTC, such as 2007-12-03T10:15:30Z, '
        + 'compliant with the `date-time` format outlined in section 5.6 of '
        + 'the RFC 3339 profile of the ISO 8601 standard for representation '
        + 'of dates and times using the Gregorian calendar.'
    ),
    serialize=serialize,
    parse_value=parse_value,
)
