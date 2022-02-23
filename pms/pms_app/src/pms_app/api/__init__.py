from fastapi import APIRouter


router = APIRouter()


@router.get("/hello-pms")
def hello():
    return "hey!"
