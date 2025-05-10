from pynamodb.attributes import UnicodeAttribute
from pynamodb.models import Model

from app.settings import config


class BaseModel(Model):
    class Meta:
        host = config.DB_HOST
        region = config.AWS_REGION

    created_at = UnicodeAttribute(null=False)
    updated_at = UnicodeAttribute(null=False)
    deleted_at = UnicodeAttribute(null=True)
