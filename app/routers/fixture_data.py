from fastapi import APIRouter

from app.utils.create_fixture_data import create_fixture_data

router = APIRouter()


@router.post("/create")
def create_data():
    create_fixture_data()

    return {"message": "Data created"}
