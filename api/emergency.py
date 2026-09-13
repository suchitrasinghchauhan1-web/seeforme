from fastapi import APIRouter


router = APIRouter(
    prefix="/emergency",
    tags=["Emergency"]
)


@router.post("/activate")
def activate_emergency():
    return {
        "status": "success",
        "message": "Emergency mode activated"
    }