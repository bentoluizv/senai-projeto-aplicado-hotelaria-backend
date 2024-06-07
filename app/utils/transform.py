from datetime import datetime
from uuid import UUID


def transform(obj: dict):
    new_obj = obj.copy()

    for k, v in new_obj.items():
        if k == "created_at" or k == "check_in" or k == "check_out":
            new_obj[k] = datetime.fromisoformat(v)

        if (
            k == "total_guests"
            or k == "single_beds"
            or k == "double_beds"
            or k == "min_nights"
            or k == "price"
        ):
            new_obj[k] = int(v)

        if k == "uuid":
            new_obj[k] = UUID(v)

        if isinstance(v, dict):
            inner_new_obj = transform(v)
            new_obj[k] = inner_new_obj

    return new_obj
