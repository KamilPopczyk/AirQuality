import json
import urllib.request
from typing import Any, List, TypeVar, Type, cast, Callable


T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


class Param:
    param_name: str
    param_formula: str
    param_code: str
    id_param: int

    def __init__(self, param_name: str, param_formula: str, param_code: str, id_param: int) -> None:
        self.param_name = param_name
        self.param_formula = param_formula
        self.param_code = param_code
        self.id_param = id_param

    @staticmethod
    def from_dict(obj: Any) -> 'Param':
        assert isinstance(obj, dict)
        param_name = from_str(obj.get("paramName"))
        param_formula = from_str(obj.get("paramFormula"))
        param_code = from_str(obj.get("paramCode"))
        id_param = from_int(obj.get("idParam"))
        return Param(param_name, param_formula, param_code, id_param)

    def to_dict(self) -> dict:
        result: dict = {}
        result["paramName"] = from_str(self.param_name)
        result["paramFormula"] = from_str(self.param_formula)
        result["paramCode"] = from_str(self.param_code)
        result["idParam"] = from_int(self.id_param)
        return result


class SensorElement:
    id: int
    station_id: int
    param: Param

    def __init__(self, id: int, station_id: int, param: Param) -> None:
        self.id = id
        self.station_id = station_id
        self.param = param

    @staticmethod
    def from_dict(obj: Any) -> 'SensorElement':
        assert isinstance(obj, dict)
        id = from_int(obj.get("id"))
        station_id = from_int(obj.get("stationId"))
        param = Param.from_dict(obj.get("param"))
        return SensorElement(id, station_id, param)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_int(self.id)
        result["stationId"] = from_int(self.station_id)
        result["param"] = to_class(Param, self.param)
        return result


def sensor_from_dict(s: Any) -> List[SensorElement]:
    return from_list(SensorElement.from_dict, s)


def sensor_to_dict(x: List[SensorElement]) -> Any:
    return from_list(lambda x: to_class(SensorElement, x), x)


if __name__ == "__main__":
    url_string = 'http://api.gios.gov.pl/pjp-api/rest/station/sensors/14'
    with urllib.request.urlopen(url_string) as url:
        json_string = str(url.read().decode())

    result = sensor_from_dict(json.loads(json_string))
    for r in result:
        print(r.param.param_name)