from pynamodb.attributes import ListAttribute
from pynamodb.attributes import UnicodeAttribute

from .base import BaseModel


class EmailTracking(BaseModel):
    class Meta(BaseModel.Meta):
        table_name = "EmailTracking"

    PK = UnicodeAttribute(hash_key=True)
    SK = UnicodeAttribute(range_key=True)

    batch_id = UnicodeAttribute()
    emails = ListAttribute(of=UnicodeAttribute)
    status = UnicodeAttribute()
    utm_source = UnicodeAttribute()
