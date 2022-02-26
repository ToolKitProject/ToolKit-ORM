from abc import ABC, abstractmethod
from ast import literal_eval
from datetime import date, datetime, time, timedelta
from decimal import Decimal as decimal
from json import dumps, loads
from typing import Generic

from toolkitorm import SQL, V
from toolkitorm.sql.dialect import BaseDialect


class BaseType(Generic[V], ABC):
    """Abstract class for SQL data types"""

    __type__: type[V]
    __type_name__: str
    __dialect__: BaseDialect
    __args__: tuple[object, ...]

    def __init__(self, *args: object) -> None:
        assert hasattr(self, "__type__")  # TODO
        if not hasattr(self, "__type_name__"):
            self.__type_name__ = type(self).__name__
        assert hasattr(self, "__dialect__")  # TODO
        self.__args__ = args

    def to_sql(self, value: V | None) -> SQL:
        """
        Get python value and return 'repr SQL' value
        """
        if value is None:
            return SQL("NULL")
        else:
            return SQL(self._to(value))

    def from_sql(self, sql: SQL) -> V | None:
        """
        Get 'not repr SQL' value and return python value
        """
        if sql.upper() == "NULL":
            return None
        else:
            return self._from(sql)

    def convert(self, value: object) -> V | None:
        """
        Get any value and return python value (Implicit conversion)
        """
        if isinstance(value, self.__type__) or value is None:
            return value
        else:
            return self.from_sql(SQL(str(value)))

    @property
    def sql_name(self) -> str:
        """Return name of the SQL type"""
        args = ",".join(map(repr, self.__args__))
        return f"{self.__type_name__.upper()}({args})"

    @abstractmethod
    def _to(self, value: V) -> str:
        pass

    @abstractmethod
    def _from(self, sql: str) -> V:
        pass


class BaseAny(BaseType[object]):
    __type__ = object

    def _to(self, value: object) -> str:
        return repr(value)

    def _from(self, sql: str) -> object:
        return literal_eval(sql)


class BaseInteger(BaseType[int]):
    __type__ = int

    def _to(self, value: int) -> str:
        return repr(value)

    def _from(self, sql: str) -> int:
        return int(sql)


class BaseFloat(BaseType[float]):
    __type__ = float

    def _to(self, value: float) -> str:
        return repr(value)

    def _from(self, sql: str) -> float:
        return float(sql)


class BaseDecimal(BaseType[decimal]):
    __type__ = decimal

    def _to(self, value: decimal) -> str:
        return repr(str(value))

    def _from(self, sql: str) -> decimal:
        return decimal(sql)


class BaseString(BaseType[str]):
    __type__ = str

    def _to(self, value: str) -> str:
        return repr(value)

    def _from(self, sql: str) -> str:
        return sql


class BaseBool(BaseType[bool]):
    __type__ = bool

    def _to(self, value: bool) -> str:
        return str(value).upper()

    def _from(self, sql: str) -> bool:
        return True if sql.upper() in ("TRUE", "YES", "ON", "1") else False


class BaseList(BaseType[list[V]]):
    __type__ = list

    def _to(self, value: list[V]) -> str:
        return repr(dumps(value))

    def _from(self, sql: str) -> list[V]:
        return loads(sql)


class BaseDict(BaseType[dict[str, V]]):
    __type__ = dict

    def _to(self, value: dict[str, V]) -> str:
        return repr(dumps(value))

    def _from(self, sql: str) -> dict[str, V]:
        return loads(sql)


class BaseDate(BaseType[date]):
    __type__ = date

    def _to(self, value: date) -> str:
        return repr(value.isoformat())

    def _from(self, sql: str) -> date:
        return date.fromisoformat(sql)


class BaseTime(BaseType[time]):
    __type__ = time

    def _to(self, value: time) -> str:
        return repr(value.isoformat())

    def _from(self, sql: str) -> time:
        return time.fromisoformat(sql)


class BaseDatetime(BaseType[datetime]):
    __type__ = datetime

    def _to(self, value: datetime) -> str:
        return repr(value.isoformat(" "))

    def _from(self, sql: str) -> datetime:
        return datetime.fromisoformat(sql)


class BaseTimedelta(BaseType[timedelta]):
    __type__ = timedelta

    def _to(self, value: timedelta) -> str:
        return repr(str(value.total_seconds()))

    def _from(self, sql: str) -> timedelta:
        return timedelta(seconds=float(sql))


__all__ = [
    "BaseType",
    "BaseAny",
    "BaseInteger",
    "BaseFloat",
    "BaseDecimal",
    "BaseString",
    "BaseBool",
    "BaseList",
    "BaseDict",
    "BaseDate",
    "BaseTime",
    "BaseDatetime",
    "BaseTimedelta",
]