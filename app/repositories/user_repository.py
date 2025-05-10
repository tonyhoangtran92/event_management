import uuid
from collections import defaultdict
from datetime import datetime
from datetime import timezone
from typing import Any, Dict, Union

from app.cache.cache_redis import redis_cache
from app.core.constants import template_mail
from app.models import User
from app.models import UserEvent
from app.services.email_service import EmailService


class UserRepository:
    table = User

    @staticmethod
    def _preprocess_create(values: Dict[str, Any]) -> Dict[str, Any]:
        now = datetime.now(timezone.utc).isoformat()
        values["user_id"] = uuid.uuid4().hex
        values["created_at"] = now
        values["updated_at"] = now
        return values

    @classmethod
    def create(cls, user_data):
        data = cls._preprocess_create(user_data)
        model = cls.table(**data)
        model.save()
        return model.attribute_values

    @classmethod
    def get(cls, user_id: Union[str, uuid.UUID]):
        model = cls.table.get(str(user_id))
        return model.attribute_values

    @classmethod
    @redis_cache(cache_key="user_event_counts")
    def get_user_event_counts(cls):
        response = UserEvent.scan()
        counts = defaultdict(lambda: {"hosted": 0, "attended": 0})
        for item in response:
            user_id = item.user_id
            if item.role == "host":
                counts[user_id]["hosted"] += 1
            else:
                counts[user_id]["attended"] += 1
        return counts

    @classmethod
    def filter_users(cls, filter):
        condition = User.PK.startswith("USER")
        if filter.company:
            condition &= User.company == filter.company
        if filter.job_title:
            condition &= User.job_title == filter.job_title
        if filter.city:
            condition &= User.city == filter.city
        if filter.state:
            condition &= User.state == filter.state

        users = list(User.scan(filter_condition=condition))

        if filter.hosted_range or filter.attended_range:
            user_event_counts = cls.get_user_event_counts()
            users = cls._filter_and_annotate_users(users, user_event_counts, filter)
        else:
            users = [u.attribute_values for u in users]

        users = sorted(users, key=lambda x: (x.get(filter.sort_by) or ""), reverse=False)

        if filter.is_send_email:
            return users

        return cls._paginate_users(users, filter)

    @classmethod
    def _filter_and_annotate_users(cls, users, counts, filter):
        """
        Filter users by event count ranges and annotate with 'hosted' and 'attended'.
        """
        filtered = []
        for user in users:
            user_id = user.user_id
            hosted = counts.get(user_id, {}).get("hosted", 0)
            attended = counts.get(user_id, {}).get("attended", 0)

            if filter.hosted_range:
                min_hosted, max_hosted = filter.hosted_range
                if not (min_hosted <= hosted <= max_hosted):
                    continue

            if filter.attended_range:
                min_attended, max_attended = filter.attended_range
                if not (min_attended <= attended <= max_attended):
                    continue

            attribute_values = user.attribute_values
            attribute_values["hosted"] = hosted
            attribute_values["attended"] = attended
            filtered.append(attribute_values)

        return filtered

    @classmethod
    def _paginate_users(cls, users, filter):
        """
        Paginate a list of users based on filter parameters.
        """
        total = len(users)
        limit = filter.limit
        page = max(1, filter.page)
        total_pages = (total + limit - 1) // limit
        start = (page - 1) * limit
        end = start + limit
        paginated = users[start:end]

        return {
            "page": page,
            "limit": limit,
            "total": total,
            "total_pages": total_pages,
            "data": paginated,
        }

    @classmethod
    def send_email(cls, users, utm_source):
        subject = template_mail.SUBJECT_SEND_EMAIL
        body = template_mail.EMAIL_TEMPLATE

        response = EmailService.send_email_to_users(users, subject, body, utm_source)

        return response
