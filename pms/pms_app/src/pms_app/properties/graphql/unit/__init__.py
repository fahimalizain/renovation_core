from graphql import GraphQLSchema
from .create import unit_create_resolver
from .update import unit_update_resolver
from .delete import unit_delete_resolver


def bind_resolvers(schema: GraphQLSchema):

    schema.mutation_type.fields["unitCreate"].resolve = \
        unit_create_resolver

    schema.mutation_type.fields["unitUpdate"].resolve = \
        unit_update_resolver

    schema.mutation_type.fields["unitDelete"].resolve = \
        unit_delete_resolver
