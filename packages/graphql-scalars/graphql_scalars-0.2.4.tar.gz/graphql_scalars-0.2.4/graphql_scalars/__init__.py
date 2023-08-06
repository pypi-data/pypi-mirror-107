__version__ = '0.2.4'

from graphql_scalars import scalars
from graphql_scalars.scalars import GraphQLDateTime, GraphQLJSON, GraphQLTimestamp, GraphQLVoid

all_scalars_defs = [GraphQLDateTime, GraphQLVoid, GraphQLTimestamp, GraphQLJSON]

__all__ = ['scalars', 'all_scalars_defs']
