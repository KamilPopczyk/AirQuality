import json
import urllib.request

from typing import Any, Optional, List, TypeVar, Type, cast, Callable


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


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


class Commune:
    commune_name: str
    district_name: str
    province_name: str

    def __init__(self, commune_name: str, district_name: str, province_name: str) -> None:
        self.commune_name = commune_name
        self.district_name = district_name
        self.province_name = province_name

    @staticmethod
    def from_dict(obj: Any) -> 'Commune':
        assert isinstance(obj, dict)
        commune_name = from_str(obj.get("communeName"))
        district_name = from_str(obj.get("districtName"))
        province_name = from_str(obj.get("provinceName"))
        return Commune(commune_name, district_name, province_name)

    def to_dict(self) -> dict:
        result: dict = {}
        result["communeName"] = from_str(self.commune_name)
        result["districtName"] = from_str(self.district_name)
        result["provinceName"] = from_str(self.province_name)
        return result


class City:
    id: int
    name: str
    commune: Commune

    def __init__(self, id: int, name: str, commune: Commune) -> None:
        self.id = id
        self.name = name
        self.commune = commune

    @staticmethod
    def from_dict(obj: Any) -> 'City':
        assert isinstance(obj, dict)
        id = from_int(obj.get("id"))
        name = from_str(obj.get("name"))
        commune = Commune.from_dict(obj.get("commune"))
        return City(id, name, commune)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_int(self.id)
        result["name"] = from_str(self.name)
        result["commune"] = to_class(Commune, self.commune)
        return result


class StationElement:
    id: int
    station_name: str
    gegr_lat: str
    gegr_lon: str
    city: City
    address_street: Optional[str]

    def __init__(self, id: int, station_name: str, gegr_lat: str, gegr_lon: str, city: City, address_street: Optional[str]) -> None:
        self.id = id
        self.station_name = station_name
        self.gegr_lat = gegr_lat
        self.gegr_lon = gegr_lon
        self.city = city
        self.address_street = address_street

    @staticmethod
    def from_dict(obj: Any) -> 'StationElement':
        assert isinstance(obj, dict)
        id = from_int(obj.get("id"))
        station_name = from_str(obj.get("stationName"))
        gegr_lat = from_str(obj.get("gegrLat"))
        gegr_lon = from_str(obj.get("gegrLon"))
        city = City.from_dict(obj.get("city"))
        address_street = from_union([from_none, from_str], obj.get("addressStreet"))
        return StationElement(id, station_name, gegr_lat, gegr_lon, city, address_street)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_int(self.id)
        result["stationName"] = from_str(self.station_name)
        result["gegrLat"] = from_str(self.gegr_lat)
        result["gegrLon"] = from_str(self.gegr_lon)
        result["city"] = to_class(City, self.city)
        result["addressStreet"] = from_union([from_none, from_str], self.address_street)
        return result


def station_from_dict(s: Any) -> List[StationElement]:
    return from_list(StationElement.from_dict, s)


def station_to_dict(x: List[StationElement]) -> Any:
    return from_list(lambda x: to_class(StationElement, x), x)


if __name__ == "__main__":
    url_string = 'http://api.gios.gov.pl/pjp-api/rest/station/findAll'
    with urllib.request.urlopen(url_string) as url:
        json_string = str(url.read().decode())

    result = station_from_dict(json.loads(json_string))
    for r in result:
        print(r.station_name)
