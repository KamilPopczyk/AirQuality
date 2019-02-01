from datetime import datetime
from typing import Optional, Any, List, TypeVar, Callable, Type, cast
import dateutil.parser
import json
import urllib.request

T = TypeVar("T")


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def to_float(x: Any) -> float:
    assert isinstance(x, float)
    return x


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


class Value:
    date: datetime
    value: Optional[float]

    def __init__(self, date: datetime, value: Optional[float]) -> None:
        self.date = date
        self.value = value

    @staticmethod
    def from_dict(obj: Any) -> 'Value':
        assert isinstance(obj, dict)
        date = from_datetime(obj.get("date"))
        value = from_union([from_none, from_float], obj.get("value"))
        return Value(date, value)

    def to_dict(self) -> dict:
        result: dict = {}
        result["date"] = self.date.isoformat()
        result["value"] = from_union([from_none, to_float], self.value)
        return result


class StationData:
    key: str
    values: List[Value]

    def __init__(self, key: str, values: List[Value]) -> None:
        self.key = key
        self.values = values

    @staticmethod
    def from_dict(obj: Any) -> 'StationData':
        assert isinstance(obj, dict)
        key = from_str(obj.get("key"))
        values = from_list(Value.from_dict, obj.get("values"))
        return StationData(key, values)

    def to_dict(self) -> dict:
        result: dict = {}
        result["key"] = from_str(self.key)
        result["values"] = from_list(lambda x: to_class(Value, x), self.values)
        return result


def station_data_from_dict(s: Any) -> StationData:
    return StationData.from_dict(s)


def station_data_to_dict(x: StationData) -> Any:
    return to_class(StationData, x)


if __name__ == "__main__":
    url_string = 'http://api.gios.gov.pl/pjp-api/rest/data/getData/92'
    with urllib.request.urlopen(url_string) as url:
        json_string = str(url.read().decode())

    result = station_data_from_dict(json.loads(json_string))
    for r in result.values:
        print(r.date, r.value)
