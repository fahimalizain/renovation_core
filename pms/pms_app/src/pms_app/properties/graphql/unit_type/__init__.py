from graphql import GraphQLSchema

from .create import unit_type_create_resolver
from .update import unit_type_update_resolver
from .delete import unit_type_delete_resolver


def bind_resolvers(schema: GraphQLSchema):
    schema.mutation_type.fields["unitTypeCreate"].resolve = \
        unit_type_create_resolver

    schema.mutation_type.fields["unitTypeUpdate"].resolve = \
        unit_type_update_resolver

    schema.mutation_type.fields["unitTypeDelete"].resolve = \
        unit_type_delete_resolver
