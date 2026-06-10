
from fastapi import APIRouter

router = APIRouter()


@router.get("/refunds")
def refunds():

    return {
        "message": "Refunds API Working"
    }