import json
import logging
from typing import NewType, Union, Dict

logger = logging.getLogger(__name__)

IntrospectionId = NewType("IntrospectionId", Union[str, int, tuple])


class Introspection:
    def __init__(self, _id, **attributes):
        if _id is None:
            raise TypeError(
                f"""No _id was provided, so no valid data comparisons can be made.
                To provide an identifier key, set the kwarg identifier=True on the attribute_key you want to correspond
                with the identifying value for the given record on introspect_return_value or introspect_object_value
                """
            )

        self._id: IntrospectionId = _id
        for k, v in attributes.items():
            self.__setattr__(k, v)

    @property
    def id(self):
        return getattr(self, self._id)

    @property
    def json(self):
        return json.dumps(vars(self))

    @property
    def as_dict(self) -> dict:
        return vars(self)

    def __repr__(self):
        string_val = ""
        for k, v in vars(self).items():
            if string_val == "":
                string_val = f"{k}={v}"
            else:
                string_val = f"{string_val}, {k}={v}"
        return f"Introspection({string_val})"

    def __eq__(self, other):
        return self.as_dict == other.as_dict

    # TODO: Make this method return a report object which can be configured for various types of output via cli args
    def compare(self, other) -> None:
        print(f"------COMPARING original: {self.id}, new: {other.id}---------")
        if self == other:
            print(f"Matched: Records with id: {self.id} are equal")
            return

        self.compare_introspection_dicts(self.as_dict, other.as_dict, parent=self.id)

    @classmethod
    def compare_introspection_dicts(cls, primary_dict, comparison_dict, parent="") -> None:
        for k, v in primary_dict.items():
            if isinstance(v, dict):
                cls.compare_introspection_dicts(v, comparison_dict.get(k, {}), parent=k)
            else:
                if v != comparison_dict.get(k):
                    print(f"MisMatch:  {parent}.{k}: {v} does not equal {comparison_dict.get(k)}")


IntrospectionsSet = NewType("IntrospectionsSet",  Dict[IntrospectionId, Introspection])