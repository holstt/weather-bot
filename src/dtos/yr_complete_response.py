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


@dataclass
class Units:
    air_pressure_at_sea_level: Optional[str] = None
    air_temperature: Optional[str] = None
    air_temperature_max: Optional[str] = None
    air_temperature_min: Optional[str] = None
    air_temperature_percentile_10: Optional[str] = None
    air_temperature_percentile_90: Optional[str] = None
    cloud_area_fraction: Optional[str] = None
    cloud_area_fraction_high: Optional[str] = None
    cloud_area_fraction_low: Optional[str] = None
    cloud_area_fraction_medium: Optional[str] = None
    dew_point_temperature: Optional[str] = None
    fog_area_fraction: Optional[str] = None
    precipitation_amount: Optional[str] = None
    precipitation_amount_max: Optional[str] = None
    precipitation_amount_min: Optional[str] = None
    probability_of_precipitation: Optional[str] = None
    probability_of_thunder: Optional[str] = None
    relative_humidity: Optional[str] = None
    ultraviolet_index_clear_sky: Optional[str] = None
    wind_from_direction: Optional[str] = None
    wind_speed: Optional[str] = None
    wind_speed_of_gust: Optional[str] = None
    wind_speed_percentile_10: Optional[str] = None
    wind_speed_percentile_90: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> "Units":
        assert isinstance(obj, dict)
        air_pressure_at_sea_level = from_union(
            [from_str, from_none], obj.get("air_pressure_at_sea_level")
        )
        air_temperature = from_union([from_str, from_none], obj.get("air_temperature"))
        air_temperature_max = from_union(
            [from_str, from_none], obj.get("air_temperature_max")
        )
        air_temperature_min = from_union(
            [from_str, from_none], obj.get("air_temperature_min")
        )
        air_temperature_percentile_10 = from_union(
            [from_str, from_none], obj.get("air_temperature_percentile_10")
        )
        air_temperature_percentile_90 = from_union(
            [from_str, from_none], obj.get("air_temperature_percentile_90")
        )
        cloud_area_fraction = from_union(
            [from_str, from_none], obj.get("cloud_area_fraction")
        )
        cloud_area_fraction_high = from_union(
            [from_str, from_none], obj.get("cloud_area_fraction_high")
        )
        cloud_area_fraction_low = from_union(
            [from_str, from_none], obj.get("cloud_area_fraction_low")
        )
        cloud_area_fraction_medium = from_union(
            [from_str, from_none], obj.get("cloud_area_fraction_medium")
        )
        dew_point_temperature = from_union(
            [from_str, from_none], obj.get("dew_point_temperature")
        )
        fog_area_fraction = from_union(
            [from_str, from_none], obj.get("fog_area_fraction")
        )
        precipitation_amount = from_union(
            [from_str, from_none], obj.get("precipitation_amount")
        )
        precipitation_amount_max = from_union(
            [from_str, from_none], obj.get("precipitation_amount_max")
        )
        precipitation_amount_min = from_union(
            [from_str, from_none], obj.get("precipitation_amount_min")
        )
        probability_of_precipitation = from_union(
            [from_str, from_none], obj.get("probability_of_precipitation")
        )
        probability_of_thunder = from_union(
            [from_str, from_none], obj.get("probability_of_thunder")
        )
        relative_humidity = from_union(
            [from_str, from_none], obj.get("relative_humidity")
        )
        ultraviolet_index_clear_sky = from_union(
            [from_str, from_none], obj.get("ultraviolet_index_clear_sky")
        )
        wind_from_direction = from_union(
            [from_str, from_none], obj.get("wind_from_direction")
        )
        wind_speed = from_union([from_str, from_none], obj.get("wind_speed"))
        wind_speed_of_gust = from_union(
            [from_str, from_none], obj.get("wind_speed_of_gust")
        )
        wind_speed_percentile_10 = from_union(
            [from_str, from_none], obj.get("wind_speed_percentile_10")
        )
        wind_speed_percentile_90 = from_union(
            [from_str, from_none], obj.get("wind_speed_percentile_90")
        )
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


@dataclass
class Summary:
    symbol_code: str
    symbol_confidence: Optional[str]

    @staticmethod
    def from_dict(obj: Any) -> "Summary":
        assert isinstance(obj, dict)
        symbol_code = from_str(obj.get("symbol_code"))
        symbol_confidence = from_union(
            [from_str, from_none], obj.get("symbol_confidence")
        )
        return Summary(symbol_code, symbol_confidence)


@dataclass
class Details:
    # Maximum air temperature in period
    air_temperature_max: Optional[float] = None
    # Minimum air temperature in period
    air_temperature_min: Optional[float] = None
    # Best estimate for amount of precipitation for this period
    precipitation_amount: Optional[float] = None
    # Maximum amount of precipitation for this period
    precipitation_amount_max: Optional[float] = None
    # Minimum amount of precipitation for this period
    precipitation_amount_min: Optional[float] = None
    # Probability of _any_ precipitation coming for this period
    probability_of_precipitation: Optional[float] = None
    # Probability of any thunder coming for this period
    probability_of_thunder: Optional[float] = None
    # Maximum ultraviolet index if sky is clear
    ultraviolet_index_clear_sky_max: Optional[float] = None

    @staticmethod
    def from_dict(obj: Any) -> "Details":
        assert isinstance(obj, dict)
        air_temperature_max = from_union(
            [from_float, from_none], obj.get("air_temperature_max")
        )
        air_temperature_min = from_union(
            [from_float, from_none], obj.get("air_temperature_min")
        )
        precipitation_amount = from_union(
            [from_float, from_none], obj.get("precipitation_amount")
        )
        precipitation_amount_max = from_union(
            [from_float, from_none], obj.get("precipitation_amount_max")
        )
        precipitation_amount_min = from_union(
            [from_float, from_none], obj.get("precipitation_amount_min")
        )
        probability_of_precipitation = from_union(
            [from_float, from_none], obj.get("probability_of_precipitation")
        )
        probability_of_thunder = from_union(
            [from_float, from_none], obj.get("probability_of_thunder")
        )
        ultraviolet_index_clear_sky_max = from_union(
            [from_float, from_none], obj.get("ultraviolet_index_clear_sky_max")
        )
        return Details(
            air_temperature_max,
            air_temperature_min,
            precipitation_amount,
            precipitation_amount_max,
            precipitation_amount_min,
            probability_of_precipitation,
            probability_of_thunder,
            ultraviolet_index_clear_sky_max,
        )


@dataclass
class Instant:
    details: Details

    @staticmethod
    def from_dict(obj: Any) -> "Instant":
        assert isinstance(obj, dict)
        details = Details.from_dict(obj.get("details"))
        return Instant(details)


@dataclass
class Next12_Hours:
    summary: Summary
    details: Optional[Details]

    @staticmethod
    def from_dict(obj: Any) -> "Next12_Hours":
        assert isinstance(obj, dict)
        summary = Summary.from_dict(obj.get("summary"))
        details = from_union([Details.from_dict, from_none], obj.get("details"))
        return Next12_Hours(summary, details)


@dataclass
class Next1_Hours:
    summary: Summary
    details: Details

    @staticmethod
    def from_dict(obj: Any) -> "Next1_Hours":
        assert isinstance(obj, dict)
        summary = Summary.from_dict(obj.get("summary"))
        # details = from_union([Details.from_dict, from_none], obj.get("details"))
        details = Details.from_dict(obj.get("details"))
        return Next1_Hours(summary, details)

    def to_dict(self) -> dict:
        result: dict = {}
        result["summary"] = to_class(Summary, self.summary)
        result["details"] = to_class(Details, self.details)
        return result


@dataclass
class Next6_Hours:
    summary: Details
    details: Optional[Details]

    @staticmethod
    def from_dict(obj: Any) -> "Next6_Hours":
        assert isinstance(obj, dict)
        summary = Details.from_dict(obj.get("summary"))
        details = from_union([Details.from_dict, from_none], obj.get("details"))
        return Next6_Hours(summary, details)

    def to_dict(self) -> dict:
        result: dict = {}
        result["summary"] = to_class(Details, self.summary)
        result["details"] = to_class(Details, self.details)
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


@dataclass
class ForecastTimeStep:
    time: datetime
    data: Data

    @staticmethod
    def from_dict(obj: Any) -> "ForecastTimeStep":
        assert isinstance(obj, dict)
        time = from_datetime(obj.get("time"))
        data = Data.from_dict(obj.get("data"))
        return ForecastTimeStep(time, data)


@dataclass
class Properties:
    meta: Meta
    timeseries: List[ForecastTimeStep]

    @staticmethod
    def from_dict(obj: Any) -> "Properties":
        assert isinstance(obj, dict)
        meta = Meta.from_dict(obj.get("meta"))
        timeseries = from_list(ForecastTimeStep.from_dict, obj.get("timeseries"))
        return Properties(meta, timeseries)


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
