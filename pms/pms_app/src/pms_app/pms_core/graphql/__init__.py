from graphql import GraphQLSchema

from .invoke_cmd import invoke_cmd_resolver


def bind_resolvers(schema: GraphQLSchema):
    from .auth import bind_resolvers as bind_auth_resolvers
    bind_auth_resolvers(schema)

    from .pms_contacts import bind_resolvers as bind_pms_contact_resolvers
    bind_pms_contact_resolvers(schema)

    from .event_logs import bind_resolvers as bind_event_log_resolvers
    bind_event_log_resolvers(schema)

    from .custom_fields import bind_resolvers as bind_custom_field_resolvers
    bind_custom_field_resolvers(schema)

    schema.mutation_type.fields["InvokeCMD"].resolve = invoke_cmd_resolver
