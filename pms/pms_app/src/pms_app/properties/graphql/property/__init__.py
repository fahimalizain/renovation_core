from graphql import GraphQLSchema
from .create import property_create_resolver
from .delete import property_delete_resolver
from .update import property_update_resolver


def bind_resolvers(schema: GraphQLSchema):

    schema.mutation_type.fields["propertyCreate"].resolve = \
        property_create_resolver

    schema.mutation_type.fields["propertyUpdate"].resolve = \
        property_update_resolver

    schema.mutation_type.fields["propertyDelete"].resolve = \
        property_delete_resolver
