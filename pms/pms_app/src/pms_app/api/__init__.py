from fastapi import APIRouter
from renovation_graphql import graphql_resolver


router = APIRouter()


@router.get("/hello-pms")
def hello():
    return "hey!"


@router.post("/graphql")
def _graphql_resolver(body: dict):
    return graphql_resolver(body=body)
