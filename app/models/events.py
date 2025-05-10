from pynamodb.attributes import UnicodeAttribute
from pynamodb.indexes import AllProjection
from pynamodb.indexes import GlobalSecondaryIndex

from .base import BaseModel


class Event(BaseModel):
    class Meta(BaseModel.Meta):
        table_name = "Events"

    PK = UnicodeAttribute(hash_key=True)
    SK = UnicodeAttribute(range_key=True, default="DETAILS")

    event_id = UnicodeAttribute()
    slug = UnicodeAttribute()
    title = UnicodeAttribute()
    description = UnicodeAttribute()
    start_at = UnicodeAttribute()
    end_at = UnicodeAttribute()
    venue = UnicodeAttribute()
    max_capacity = UnicodeAttribute()
    owner = UnicodeAttribute()


class EventIdIndex(GlobalSecondaryIndex):
    class Meta:
        index_name = "event-id-index"
        projection = AllProjection()
        read_capacity_units = 1000
        write_capacity_units = 1000

    event_id = UnicodeAttribute(hash_key=True)
    user_event_pk = UnicodeAttribute(range_key=True)


class UserEvent(BaseModel):
    class Meta(BaseModel.Meta):
        table_name = "UserEvents"

    PK = UnicodeAttribute(hash_key=True)
    SK = UnicodeAttribute(range_key=True)

    user_id = UnicodeAttribute()
    event_id = UnicodeAttribute()
    role = UnicodeAttribute()  # 'host' or 'attendee'

    event_id_index = EventIdIndex()
