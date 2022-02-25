from fastapi import APIRouter

router = APIRouter()


@router.get("/hello-todo")
def hello():
    return "hey!"
