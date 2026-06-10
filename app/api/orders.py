
from fastapi import APIRouter

router = APIRouter()


@router.get("/orders")
def orders():

    return {
        "message": "Orders API Working"
    }