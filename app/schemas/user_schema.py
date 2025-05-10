from pydantic import BaseModel


class UserFilter(BaseModel):
    company: str = ""
    job_title: str = ""
    city: str = ""
    state: str = ""
    hosted_range: tuple[int, int] | None = None
    attended_range: tuple[int, int] | None = None
    page: int = 1
    limit: int = 10
    sort_by: str = "first_name"
    is_send_email: bool = False
    batch_send_email: int = 100
