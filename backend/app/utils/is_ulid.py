from ulid import ULID


def is_ulid(id: str):
    try:
        ULID.from_str(id)

        return True

    except ValueError:
        return False
