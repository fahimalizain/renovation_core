from graphql import GraphQLSchema
from .get_event_types import get_event_types_resolver
from .get_events import get_events_resolver
from .get_event_thread import get_event_thread_resolver

from .create_event_log import create_event_log_resolver
from .delete_event_log import delete_event_log_resolver


def bind_resolvers(schema: GraphQLSchema):
    schema.query_type.fields["EventLogGetEventTypes"].resolve = get_event_types_resolver
    schema.query_type.fields["EventLogGetEvents"].resolve = get_events_resolver
    schema.query_type.fields["EventLogGetEventThread"].resolve = get_event_thread_resolver

    schema.mutation_type.fields["EventLogCreate"].resolve = create_event_log_resolver
    schema.mutation_type.fields["EventLogDelete"].resolve = delete_event_log_resolver
