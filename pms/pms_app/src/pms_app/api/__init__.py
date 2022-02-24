from fastapi import APIRouter
from renovation_graphql import graphql_resolver as _graphql_resolver


router = APIRouter()


@router.get("/hello-pms")
def hello():
    return "hey!"


@router.post("/graphql")
async def graphql_resolver(body: dict):
    return await _graphql_resolver(body=body)
