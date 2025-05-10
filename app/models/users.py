from pynamodb.attributes import UnicodeAttribute
from pynamodb.indexes import AllProjection
from pynamodb.indexes import GlobalSecondaryIndex

from .base import BaseModel


class CompanyIndex(GlobalSecondaryIndex):
    class Meta:
        index_name = "company-index"
        projection = AllProjection()
        read_capacity_units = 1000
        write_capacity_units = 1000

    company = UnicodeAttribute(hash_key=True)
    user_pk = UnicodeAttribute(range_key=True)


class CityStateIndex(GlobalSecondaryIndex):
    class Meta:
        index_name = "city-state-index"
        projection = AllProjection()
        read_capacity_units = 1000
        write_capacity_units = 1000

    city = UnicodeAttribute(hash_key=True)
    state = UnicodeAttribute(range_key=True)


class User(BaseModel):
    class Meta(BaseModel.Meta):
        table_name = "Users"

    PK = UnicodeAttribute(hash_key=True)
    SK = UnicodeAttribute(range_key=True, default="PROFILE")

    user_id = UnicodeAttribute()
    first_name = UnicodeAttribute()
    last_name = UnicodeAttribute()
    phone_number = UnicodeAttribute()
    email = UnicodeAttribute()
    avatar = UnicodeAttribute()
    gender = UnicodeAttribute()
    job_title = UnicodeAttribute()
    company = UnicodeAttribute()
    city = UnicodeAttribute()
    state = UnicodeAttribute()

    company_index = CompanyIndex()
    city_state_index = CityStateIndex()
