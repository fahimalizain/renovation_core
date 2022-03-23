from graphql import GraphQLSchema

from .invoke_cmd import invoke_cmd_resolver


def bind_resolvers(schema: GraphQLSchema):
    from .pms_contacts import bind_resolvers as bind_pms_contact_resolvers
    bind_pms_contact_resolvers(schema)

    schema.mutation_type.fields["InvokeCMD"].resolve = invoke_cmd_resolver
