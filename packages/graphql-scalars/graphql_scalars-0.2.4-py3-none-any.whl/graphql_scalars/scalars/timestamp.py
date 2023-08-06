__all__ = ['serialize', 'parse_value', 'GraphQLTimestamp']

from datetime import date, datetime, timezone
from typing import Union

import arrow
from arrow import Arrow
from graphql import GraphQLScalarType


def serialize(value: Union[datetime, date, Arrow, str]) -> int:
    if not isinstance(value, (datetime, date, Arrow, str)):
        raise TypeError('Timestamp cannot represent non-datetime/date/Arrow/str type')
    dt = arrow.get(value)
    return int(dt.timestamp() * 1000)


def parse_value(value: Union[int, float]) -> datetime:
    # for historic reason, bool is a subclass of int,
    # so isinstance(True, int) is always True
    if type(value) in [int, float]:
        # the fact that arrow.get() can receive both seconds timestamp and ms/us timestamp
        # is not desired by us, so here uses datetime.fromtimestamp()
        dt = datetime.fromtimestamp(value / 1000, timezone.utc)
        return dt
    else:
        raise TypeError('Timestamp cannot be represented by non-int/float type')


GraphQLTimestamp = GraphQLScalarType(
    name='Timestamp',
    description='A Epoch Unix timestamp integer in milliseconds, such as 1621998739087',
    serialize=serialize,
    parse_value=parse_value,
)
