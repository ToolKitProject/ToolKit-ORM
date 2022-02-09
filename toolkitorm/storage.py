"""FIXME: DOCS"""
from typing import Generic

from toolkitorm.types import V
from toolkitorm.types.base import SQL, BaseType


class Data(Generic[V]):
    value: V | None
    value_type: BaseType[V]

    def __init__(self, value: object, value_type: BaseType[V]) -> None:
        self.value = None
        self.value_type = value_type

        self.set(value)

    def to_sql(self) -> SQL:
        return self.value_type.to_sql(self.value)

    def set(self, value: object) -> None:
        if isinstance(value, self.value_type.__type__) or value is None:
            self.value = value
        else:
            try:
                self.value = self.value_type.from_sql(SQL(str(value)))
            except Exception:
                raise RuntimeError  # TODO


class Storage:
    storage: dict[str, Data]

    def __init__(self) -> None:
        self.storage = {}

    def get(self, name: str) -> Data:
        assert name in self.storage, "Column not found"
        return self.storage[name]

    def add(self, name: str, value: object, value_type: BaseType[V]) -> None:
        assert name not in self.storage, "Column already exist"
        self.storage[name] = Data(value, value_type)
