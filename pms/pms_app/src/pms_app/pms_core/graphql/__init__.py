from graphql import GraphQLSchema
from .add_contact import add_contact_resolver
from .update_contact import update_contact_resolver
from .delete_contact import delete_contact_resolver
from .invoke_cmd import invoke_cmd_resolver


def bind_resolvers(schema: GraphQLSchema):
    schema.mutation_type.fields["ContactAdd"].resolve = add_contact_resolver
    schema.mutation_type.fields["ContactUpdate"].resolve = update_contact_resolver
    schema.mutation_type.fields["ContactDelete"].resolve = delete_contact_resolver

    schema.mutation_type.fields["InvokeCMD"].resolve = invoke_cmd_resolver
