from graphql import GraphQLSchema
from .get_event_types import get_event_types_resolver


def bind_resolvers(schema: GraphQLSchema):
    schema.query_type.fields["EventLogGetEventTypes"].resolve = get_event_types_resolver
