from graphql import GraphQLSchema
from .get_event_types import get_event_types_resolver
from .get_events import get_events_resolver
from .get_event_thread import get_event_thread_resolver


def bind_resolvers(schema: GraphQLSchema):
    schema.query_type.fields["EventLogGetEventTypes"].resolve = get_event_types_resolver
    schema.query_type.fields["EventLogGetEvents"].resolve = get_events_resolver
    schema.query_type.fields["EventLogGetEventThread"].resolve = get_event_thread_resolver
