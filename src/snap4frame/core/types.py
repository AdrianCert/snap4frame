import copy
import dataclasses
from typing import Any, Dict, Iterable, Tuple, Union


def type2dict(obj: Any, own_serialization=True) -> Union[Dict[str, Any], Any]:  # noqa: PLR0911
    if isinstance(obj, TypedBase) and own_serialization:
        return obj.as_dict()

    if dataclasses.is_dataclass(obj):
        result = []
        for f in dataclasses.fields(obj):
            value = type2dict(getattr(obj, f.name))
            result.append((f.name, value))

        if hasattr(obj, "SerializeMeta") and isinstance(obj, TypedBase):
            return obj.__serialize_meta___(result)
        return dict(result)

    elif isinstance(obj, tuple) and hasattr(obj, "_fields"):
        return type(obj)(*[type2dict(v) for v in obj])

    elif isinstance(obj, (list, set, frozenset, tuple)):
        return [type2dict(v) for v in obj]

    elif isinstance(obj, dict):
        return {k: type2dict(v) for k, v in obj.items()}

    else:
        return copy.deepcopy(obj)


class TypedBase:
    __dataclass_fields__: dict

    def __serialize_meta___(
        self, kv_pairs: Iterable[Tuple[str, Any]]
    ) -> Dict[str, Any]:
        """
        Serializes the fields of the object based on key-value pairs.

        Args:
            kv_pairs (Iterable[Tuple[str, Any]]): The key-value pairs representing the fields.

        Returns:
            Dict[str, Any]: The serialized metadata as a dictionary.
        """
        cast_handler = getattr(self, "SerializeMeta")
        filter_handler = getattr(cast_handler, "filter")

        used_keys = set()

        result = {
            k: used_keys.add(k)
            or (getattr(cast_handler, k)(self, v) if hasattr(cast_handler, k) else v)
            for k, v in kv_pairs
            if not filter_handler or filter_handler(k)
        }

        extend_values = (
            cast_handler.__dict__.keys()
            - used_keys
            - {"filter", "__module__", "__doc__", "__dict__", "__weakref__"}
        )

        if extend_values:
            for k in extend_values:
                result[k] = getattr(cast_handler, k)(self)

        return result

    def as_dict(self):
        return type2dict(self, own_serialization=False)
