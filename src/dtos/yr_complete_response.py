# pyright: basic

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, Type, TypeVar, cast

import dateutil.parser

T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def to_float(x: Any) -> float:
    assert isinstance(x, float)
    return x


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_dict(f: Callable[[Any], T], x: Any) -> Dict[str, T]:
    assert isinstance(x, dict)
    return {k: f(v) for (k, v) in x.items()}


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


@dataclass
class Geometry:
    type: str
    coordinates: List[float]

    @staticmethod
    def from_dict(obj: Any) -> "Geometry":
        assert isinstance(obj, dict)
        type = from_str(obj.get("type"))
        coordinates = from_list(from_float, obj.get("coordinates"))
        return Geometry(type, coordinates)

    def to_dict(self) -> dict:
        result: dict = {}
        result["type"] = from_str(self.type)
        result["coordinates"] = from_list(to_float, self.coordinates)
        return result


@dataclass
class Units:
    air_pressure_at_sea_level: str
    air_temperature: str
    air_temperature_max: str
    air_temperature_min: str
    air_temperature_percentile_10: str
    air_temperature_percentile_90: str
    cloud_area_fraction: str
    cloud_area_fraction_high: str
    cloud_area_fraction_low: str
    cloud_area_fraction_medium: str
    dew_point_temperature: str
    fog_area_fraction: str
    precipitation_amount: str
    precipitation_amount_max: str
    precipitation_amount_min: str
    probability_of_precipitation: str
    probability_of_thunder: str
    relative_humidity: str
    ultraviolet_index_clear_sky: int
    wind_from_direction: str
    wind_speed: str
    wind_speed_of_gust: str
    wind_speed_percentile_10: str
    wind_speed_percentile_90: str

    @staticmethod
    def from_dict(obj: Any) -> "Units":
        assert isinstance(obj, dict)
        air_pressure_at_sea_level = from_str(obj.get("air_pressure_at_sea_level"))
        air_temperature = from_str(obj.get("air_temperature"))
        air_temperature_max = from_str(obj.get("air_temperature_max"))
        air_temperature_min = from_str(obj.get("air_temperature_min"))
        air_temperature_percentile_10 = from_str(
            obj.get("air_temperature_percentile_10")
        )
        air_temperature_percentile_90 = from_str(
            obj.get("air_temperature_percentile_90")
        )
        cloud_area_fraction = from_str(obj.get("cloud_area_fraction"))
        cloud_area_fraction_high = from_str(obj.get("cloud_area_fraction_high"))
        cloud_area_fraction_low = from_str(obj.get("cloud_area_fraction_low"))
        cloud_area_fraction_medium = from_str(obj.get("cloud_area_fraction_medium"))
        dew_point_temperature = from_str(obj.get("dew_point_temperature"))
        fog_area_fraction = from_str(obj.get("fog_area_fraction"))
        precipitation_amount = from_str(obj.get("precipitation_amount"))
        precipitation_amount_max = from_str(obj.get("precipitation_amount_max"))
        precipitation_amount_min = from_str(obj.get("precipitation_amount_min"))
        probability_of_precipitation = from_str(obj.get("probability_of_precipitation"))
        probability_of_thunder = from_str(obj.get("probability_of_thunder"))
        relative_humidity = from_str(obj.get("relative_humidity"))
        ultraviolet_index_clear_sky = int(
            from_str(obj.get("ultraviolet_index_clear_sky"))
        )
        wind_from_direction = from_str(obj.get("wind_from_direction"))
        wind_speed = from_str(obj.get("wind_speed"))
        wind_speed_of_gust = from_str(obj.get("wind_speed_of_gust"))
        wind_speed_percentile_10 = from_str(obj.get("wind_speed_percentile_10"))
        wind_speed_percentile_90 = from_str(obj.get("wind_speed_percentile_90"))
        return Units(
            air_pressure_at_sea_level,
            air_temperature,
            air_temperature_max,
            air_temperature_min,
            air_temperature_percentile_10,
            air_temperature_percentile_90,
            cloud_area_fraction,
            cloud_area_fraction_high,
            cloud_area_fraction_low,
            cloud_area_fraction_medium,
            dew_point_temperature,
            fog_area_fraction,
            precipitation_amount,
            precipitation_amount_max,
            precipitation_amount_min,
            probability_of_precipitation,
            probability_of_thunder,
            relative_humidity,
            ultraviolet_index_clear_sky,
            wind_from_direction,
            wind_speed,
            wind_speed_of_gust,
            wind_speed_percentile_10,
            wind_speed_percentile_90,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        result["air_pressure_at_sea_level"] = from_str(self.air_pressure_at_sea_level)
        result["air_temperature"] = from_str(self.air_temperature)
        result["air_temperature_max"] = from_str(self.air_temperature_max)
        result["air_temperature_min"] = from_str(self.air_temperature_min)
        result["air_temperature_percentile_10"] = from_str(
            self.air_temperature_percentile_10
        )
        result["air_temperature_percentile_90"] = from_str(
            self.air_temperature_percentile_90
        )
        result["cloud_area_fraction"] = from_str(self.cloud_area_fraction)
        result["cloud_area_fraction_high"] = from_str(self.cloud_area_fraction_high)
        result["cloud_area_fraction_low"] = from_str(self.cloud_area_fraction_low)
        result["cloud_area_fraction_medium"] = from_str(self.cloud_area_fraction_medium)
        result["dew_point_temperature"] = from_str(self.dew_point_temperature)
        result["fog_area_fraction"] = from_str(self.fog_area_fraction)
        result["precipitation_amount"] = from_str(self.precipitation_amount)
        result["precipitation_amount_max"] = from_str(self.precipitation_amount_max)
        result["precipitation_amount_min"] = from_str(self.precipitation_amount_min)
        result["probability_of_precipitation"] = from_str(
            self.probability_of_precipitation
        )
        result["probability_of_thunder"] = from_str(self.probability_of_thunder)
        result["relative_humidity"] = from_str(self.relative_humidity)
        result["ultraviolet_index_clear_sky"] = from_str(
            str(self.ultraviolet_index_clear_sky)
        )
        result["wind_from_direction"] = from_str(self.wind_from_direction)
        result["wind_speed"] = from_str(self.wind_speed)
        result["wind_speed_of_gust"] = from_str(self.wind_speed_of_gust)
        result["wind_speed_percentile_10"] = from_str(self.wind_speed_percentile_10)
        result["wind_speed_percentile_90"] = from_str(self.wind_speed_percentile_90)
        return result


@dataclass
class Meta:
    updated_at: datetime
    units: Units

    @staticmethod
    def from_dict(obj: Any) -> "Meta":
        assert isinstance(obj, dict)
        updated_at = from_datetime(obj.get("updated_at"))
        units = Units.from_dict(obj.get("units"))
        return Meta(updated_at, units)

    def to_dict(self) -> dict:
        result: dict = {}
        result["updated_at"] = self.updated_at.isoformat()
        result["units"] = to_class(Units, self.units)
        return result


@dataclass
class Instant:
    details: Dict[str, float]

    @staticmethod
    def from_dict(obj: Any) -> "Instant":
        assert isinstance(obj, dict)
        details = from_dict(from_float, obj.get("details"))
        return Instant(details)

    def to_dict(self) -> dict:
        result: dict = {}
        result["details"] = from_dict(to_float, self.details)
        return result


@dataclass
class Next12_HoursDetails:
    probability_of_precipitation: float

    @staticmethod
    def from_dict(obj: Any) -> "Next12_HoursDetails":
        assert isinstance(obj, dict)
        probability_of_precipitation = from_float(
            obj.get("probability_of_precipitation")
        )
        return Next12_HoursDetails(probability_of_precipitation)

    def to_dict(self) -> dict:
        result: dict = {}
        result["probability_of_precipitation"] = to_float(
            self.probability_of_precipitation
        )
        return result


@dataclass
class Next12_HoursSummary:
    symbol_code: str
    symbol_confidence: str

    @staticmethod
    def from_dict(obj: Any) -> "Next12_HoursSummary":
        assert isinstance(obj, dict)
        symbol_code = from_str(obj.get("symbol_code"))
        symbol_confidence = from_str(obj.get("symbol_confidence"))
        return Next12_HoursSummary(symbol_code, symbol_confidence)

    def to_dict(self) -> dict:
        result: dict = {}
        result["symbol_code"] = from_str(self.symbol_code)
        result["symbol_confidence"] = from_str(self.symbol_confidence)
        return result


@dataclass
class Next12_Hours:
    summary: Next12_HoursSummary
    details: Next12_HoursDetails

    @staticmethod
    def from_dict(obj: Any) -> "Next12_Hours":
        assert isinstance(obj, dict)
        summary = Next12_HoursSummary.from_dict(obj.get("summary"))
        details = Next12_HoursDetails.from_dict(obj.get("details"))
        return Next12_Hours(summary, details)

    def to_dict(self) -> dict:
        result: dict = {}
        result["summary"] = to_class(Next12_HoursSummary, self.summary)
        result["details"] = to_class(Next12_HoursDetails, self.details)
        return result


@dataclass
class Next1_HoursDetails:
    precipitation_amount: float
    precipitation_amount_max: float
    precipitation_amount_min: float
    probability_of_precipitation: float
    probability_of_thunder: float

    @staticmethod
    def from_dict(obj: Any) -> "Next1_HoursDetails":
        assert isinstance(obj, dict)
        precipitation_amount = from_float(obj.get("precipitation_amount"))
        precipitation_amount_max = from_float(obj.get("precipitation_amount_max"))
        precipitation_amount_min = from_float(obj.get("precipitation_amount_min"))
        probability_of_precipitation = from_float(
            obj.get("probability_of_precipitation")
        )
        probability_of_thunder = from_float(obj.get("probability_of_thunder"))
        return Next1_HoursDetails(
            precipitation_amount,
            precipitation_amount_max,
            precipitation_amount_min,
            probability_of_precipitation,
            probability_of_thunder,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        result["precipitation_amount"] = to_float(self.precipitation_amount)
        result["precipitation_amount_max"] = to_float(self.precipitation_amount_max)
        result["precipitation_amount_min"] = to_float(self.precipitation_amount_min)
        result["probability_of_precipitation"] = to_float(
            self.probability_of_precipitation
        )
        result["probability_of_thunder"] = to_float(self.probability_of_thunder)
        return result


@dataclass
class Next1_HoursSummary:
    symbol_code: str

    @staticmethod
    def from_dict(obj: Any) -> "Next1_HoursSummary":
        assert isinstance(obj, dict)
        symbol_code = from_str(obj.get("symbol_code"))
        return Next1_HoursSummary(symbol_code)

    def to_dict(self) -> dict:
        result: dict = {}
        result["symbol_code"] = from_str(self.symbol_code)
        return result


@dataclass
class Next1_Hours:
    summary: Next1_HoursSummary
    details: Next1_HoursDetails

    @staticmethod
    def from_dict(obj: Any) -> "Next1_Hours":
        assert isinstance(obj, dict)
        summary = Next1_HoursSummary.from_dict(obj.get("summary"))
        details = Next1_HoursDetails.from_dict(obj.get("details"))
        return Next1_Hours(summary, details)

    def to_dict(self) -> dict:
        result: dict = {}
        result["summary"] = to_class(Next1_HoursSummary, self.summary)
        result["details"] = to_class(Next1_HoursDetails, self.details)
        return result


@dataclass
class Next6_HoursDetails:
    air_temperature_max: float
    air_temperature_min: float
    precipitation_amount: float
    precipitation_amount_max: float
    precipitation_amount_min: float
    probability_of_precipitation: float

    @staticmethod
    def from_dict(obj: Any) -> "Next6_HoursDetails":
        assert isinstance(obj, dict)
        air_temperature_max = from_float(obj.get("air_temperature_max"))
        air_temperature_min = from_float(obj.get("air_temperature_min"))
        precipitation_amount = from_float(obj.get("precipitation_amount"))
        precipitation_amount_max = from_float(obj.get("precipitation_amount_max"))
        precipitation_amount_min = from_float(obj.get("precipitation_amount_min"))
        probability_of_precipitation = from_float(
            obj.get("probability_of_precipitation")
        )
        return Next6_HoursDetails(
            air_temperature_max,
            air_temperature_min,
            precipitation_amount,
            precipitation_amount_max,
            precipitation_amount_min,
            probability_of_precipitation,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        result["air_temperature_max"] = to_float(self.air_temperature_max)
        result["air_temperature_min"] = to_float(self.air_temperature_min)
        result["precipitation_amount"] = to_float(self.precipitation_amount)
        result["precipitation_amount_max"] = to_float(self.precipitation_amount_max)
        result["precipitation_amount_min"] = to_float(self.precipitation_amount_min)
        result["probability_of_precipitation"] = to_float(
            self.probability_of_precipitation
        )
        return result


@dataclass
class Next6_Hours:
    summary: Next1_HoursSummary
    details: Next6_HoursDetails

    @staticmethod
    def from_dict(obj: Any) -> "Next6_Hours":
        assert isinstance(obj, dict)
        summary = Next1_HoursSummary.from_dict(obj.get("summary"))
        details = Next6_HoursDetails.from_dict(obj.get("details"))
        return Next6_Hours(summary, details)

    def to_dict(self) -> dict:
        result: dict = {}
        result["summary"] = to_class(Next1_HoursSummary, self.summary)
        result["details"] = to_class(Next6_HoursDetails, self.details)
        return result


@dataclass
class Data:
    instant: Instant
    next_12__hours: Optional[Next12_Hours] = None
    next_1__hours: Optional[Next1_Hours] = None
    next_6__hours: Optional[Next6_Hours] = None

    @staticmethod
    def from_dict(obj: Any) -> "Data":
        assert isinstance(obj, dict)
        instant = Instant.from_dict(obj.get("instant"))
        next_12__hours = from_union(
            [Next12_Hours.from_dict, from_none], obj.get("next_12_hours")
        )
        next_1__hours = from_union(
            [Next1_Hours.from_dict, from_none], obj.get("next_1_hours")
        )
        next_6__hours = from_union(
            [Next6_Hours.from_dict, from_none], obj.get("next_6_hours")
        )
        return Data(instant, next_12__hours, next_1__hours, next_6__hours)

    def to_dict(self) -> dict:
        result: dict = {}
        result["instant"] = to_class(Instant, self.instant)
        result["next_12_hours"] = from_union(
            [lambda x: to_class(Next12_Hours, x), from_none], self.next_12__hours
        )
        result["next_1_hours"] = from_union(
            [lambda x: to_class(Next1_Hours, x), from_none], self.next_1__hours
        )
        result["next_6_hours"] = from_union(
            [lambda x: to_class(Next6_Hours, x), from_none], self.next_6__hours
        )
        return result


@dataclass
class Timesery:
    time: datetime
    data: Data

    @staticmethod
    def from_dict(obj: Any) -> "Timesery":
        assert isinstance(obj, dict)
        time = from_datetime(obj.get("time"))
        data = Data.from_dict(obj.get("data"))
        return Timesery(time, data)

    def to_dict(self) -> dict:
        result: dict = {}
        result["time"] = self.time.isoformat()
        result["data"] = to_class(Data, self.data)
        return result


@dataclass
class Properties:
    meta: Meta
    timeseries: List[Timesery]

    @staticmethod
    def from_dict(obj: Any) -> "Properties":
        assert isinstance(obj, dict)
        meta = Meta.from_dict(obj.get("meta"))
        timeseries = from_list(Timesery.from_dict, obj.get("timeseries"))
        return Properties(meta, timeseries)

    def to_dict(self) -> dict:
        result: dict = {}
        result["meta"] = to_class(Meta, self.meta)
        result["timeseries"] = from_list(
            lambda x: to_class(Timesery, x), self.timeseries
        )
        return result


@dataclass
class YrCompleteResponse:
    type: str
    geometry: Geometry
    properties: Properties

    @staticmethod
    def from_dict(obj: Any) -> "YrCompleteResponse":
        assert isinstance(obj, dict)
        type = from_str(obj.get("type"))
        geometry = Geometry.from_dict(obj.get("geometry"))
        properties = Properties.from_dict(obj.get("properties"))
        return YrCompleteResponse(type, geometry, properties)
