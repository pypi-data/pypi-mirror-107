import attr


@attr.s(slots=True)
class Serialize:
    custom_serializer_path = []