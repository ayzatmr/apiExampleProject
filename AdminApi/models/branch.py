from schematics.models import Model
from schematics.types import StringType, IntType, ListType, ModelType, FloatType

WEEK_DAYS = ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]


class Location(Model):
    lng = FloatType(required=True)
    lat = FloatType(required=True)


class CityInfo(Model):
    placeId = StringType(required=True)
    name = StringType(required=True)


class AdminBranch(Model):
    id = IntType(required=True)
    location = ModelType(Location)
    addressDescription = StringType(required=False)
    phones = ListType(StringType)
    address = StringType(required=True)
    deliveryOptions = ListType(StringType(required=False))


class AdminBranchRows(Model):
    rows = ListType(ModelType(AdminBranch), required=True)
    total = IntType(required=True)
