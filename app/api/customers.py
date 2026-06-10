
from fastapi import APIRouter

router = APIRouter()


@router.get("/customers")
def customers():

    return {
        "message": "Customers API Working"
    }