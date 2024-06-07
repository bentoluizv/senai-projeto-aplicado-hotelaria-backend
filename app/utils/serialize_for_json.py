from datetime import datetime
from uuid import UUID


def serialize_for_json(obj: dict):
    new_obj = obj.copy()

    for k, v in new_obj.items():
        if isinstance(v, datetime):
            new_obj[k] = v.isoformat()

        if isinstance(v, UUID):
            new_obj[k] = str(v)

        if isinstance(v, dict):
            inner_new_obj = serialize_for_json(v)
            new_obj[k] = inner_new_obj

    return new_obj
