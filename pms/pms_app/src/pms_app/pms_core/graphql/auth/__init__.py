from graphql import GraphQLSchema
from .get_me import get_me_resolver
from .token_create import token_create_resolver
from .token_refresh import token_refresh_resolver


def bind_resolvers(schema: GraphQLSchema):
    schema.query_type.fields["authGetMe"].resolve = get_me_resolver
    schema.mutation_type.fields["authTokenCreate"].resolve = token_create_resolver
    schema.mutation_type.fields["authTokenRefresh"].resolve = token_refresh_resolver
