from .introspection import Introspection

INTROSPECTION_DICT = {}


def introspect_return_value(key_name, identifier=False):
    def outer_wrapper(func):
        def wraps(self=None, *args, **kwargs):
            value = func(self, *args, **kwargs) if self else func(*args, **kwargs)
            INTROSPECTION_DICT[key_name] = value
            if identifier:
                INTROSPECTION_DICT["_id"] = key_name
            return value

        return wraps

    return outer_wrapper


def introspect_object_value(
    key_name, object_property, nested_property_value=None, identifier=False
):
    def outer_wrapper(func):
        def wraps(self=None, *args, **kwargs):
            if nested_property_value:
                outer_value = getattr(self, object_property)
                try:
                    value = getattr(outer_value, nested_property_value)
                except AttributeError:
                    value = outer_value.get(nested_property_value)
            else:
                value = getattr(self, object_property)

            INTROSPECTION_DICT[key_name] = value
            if identifier:
                INTROSPECTION_DICT["_id"] = key_name

            return func(self, *args, **kwargs)

        return wraps

    return outer_wrapper


class Introspect:
    def __init__(self, file="./introspection.txt"):
        self.file = file

    def __enter__(self):
        pass

    def __exit__(self, exc, exc_type, trace):
        introspection = self.build_introspection(INTROSPECTION_DICT)
        self.write_introspected_data(introspection)

    def write_introspected_data(self, introspection: Introspection):
        with open(self.file, "a") as file:
            file.writelines([introspection.json, "\n"])

    @staticmethod
    def build_introspection(introspection_dict):
        _id = introspection_dict.get("_id")
        attributes = {k: v for k, v in introspection_dict.items() if k != "_id"}
        return Introspection(_id=_id, **attributes)


def introspect(func):
    def wraps(self=None, *args, **kwargs):
        with Introspect():
            return func(self, *args, **kwargs) if self else func(*args, **kwargs)

    return wraps
