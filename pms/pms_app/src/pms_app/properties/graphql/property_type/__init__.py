from graphql import GraphQLSchema

from .create import property_type_create_resolver
from .update import property_type_update_resolver
from .delete import property_type_delete_resolver


def bind_resolvers(schema: GraphQLSchema):
    schema.mutation_type.fields["propertyTypeCreate"].resolve = \
        property_type_create_resolver

    schema.mutation_type.fields["propertyTypeUpdate"].resolve = \
        property_type_update_resolver

    schema.mutation_type.fields["propertyTypeDelete"].resolve = \
        property_type_delete_resolver
