from fastapi import APIRouter

from app.core.logger import logger
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserFilter

router = APIRouter()


@router.get("/{user_id}")
def get_user(user_id: str):
    data = UserRepository().get(user_id)
    return {"message": "User get", "user": data}


@router.post("/filter")
async def get_user_list(filter: UserFilter):
    return UserRepository().filter_users(filter)


@router.post("/send-email")
async def send_email_endpoint(filter: UserFilter, utm_source: str = "email_campaign"):
    users = UserRepository().filter_users(filter)
    len_users = len(users)
    batch_size = filter.batch_send_email if filter.batch_send_email else 100
    filter.is_send_email = True

    batches = [users[i : i + batch_size] for i in range(0, len_users, batch_size)]

    fail_count = 0

    for batch in batches:
        response = UserRepository().send_email(batch, utm_source)
        fail_count += response.get("failed", 0)

    logger.info(f"Emails sent in {len(batches)} batches. Failed {fail_count} emails")

    return {"message": f"Emails sent in {len(batches)} batches. Failed {fail_count} emails"}
