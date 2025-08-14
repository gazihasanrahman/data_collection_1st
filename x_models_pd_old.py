import json
import glob
import pandas as pd
from pydantic import BaseModel, field_validator, Field
from datetime import datetime, timedelta, date
from dateutil.parser import parse
from typing import List, Optional, Union, Dict, Any


# # Mixin classes for datetime parsing
# class TimestampMixin:
#     @field_validator('timestamp', mode='before')
#     @classmethod
#     def parse_timestamp(cls, v):
#         if isinstance(v, str):
#             return parse(v)
#         return v

# class DateTimeFieldsMixin:
#     @field_validator('posttime', 'estimatedPosttime', 'offTime', mode='before')
#     @classmethod
#     def parse_datetime_fields(cls, v):
#         if isinstance(v, str):
#             return parse(v)
#         return v

# class DateMixin:
#     @field_validator('date', mode='before')
#     @classmethod
#     def parse_date(cls, v):
#         if isinstance(v, str):
#             return datetime.strptime(v, '%Y-%m-%d').date()
#         return v


# # Equipment model
# class Equipment(BaseModel):
#     code: Optional[str] = None
#     description: Optional[str] = None



# class Purse(BaseModel):
#     value: Optional[str] = None
#     ranks: Optional[str] = None
#     unit: Optional[str] = None


# class SexRestriction(BaseModel):
#     value: Optional[str] = None
#     description: Optional[str] = None


# class AgeRestriction(BaseModel):
#     value: Optional[str] = None
#     description: Optional[str] = None


# class RaceType(BaseModel):
#     type: Optional[str] = None
#     subtype: Optional[str] = None
#     description: Optional[str] = None


# class TrackSurface(BaseModel):
#     value: Optional[str] = None

# class Distance(BaseModel):
#     value: Optional[str] = None
#     unit: Optional[str] = None
#     publishedText: Optional[str] = None


# class Race(BaseModel, DateTimeFieldsMixin):
#     id: str
#     type: Optional[str] = None
#     number: str
#     runnercount: Optional[int] = None
#     posttime: Optional[datetime] = None
#     estimatedPosttime: Optional[datetime] = None
#     offTime: Optional[datetime] = None
#     weather: Optional[str] = None
#     going: Optional[str] = None
#     name: Optional[str] = None
#     status: Optional[str] = None
#     statusHistory: Optional[List[StatusHistory]] = []
#     isdst: Optional[bool] = None
#     timezoneOffset: Optional[int] = None
#     tracksurface: TrackSurface = Field(default_factory=TrackSurface)
#     overround: Optional[str] = None
#     overround_selection: Optional[str] = None
#     entries: Optional[List[Entry]] = []
#     result: Optional[str] = None
#     comment: Optional[str] = None
#     distance: Distance = Field(default_factory=Distance)
#     breed: Optional[str] = None
#     racetype: RaceType = Field(default_factory=RaceType)
#     sexrestriction: SexRestriction = Field(default_factory=SexRestriction)
#     agerestriction: AgeRestriction = Field(default_factory=AgeRestriction)
#     purse: Purse = Field(default_factory=Purse)
#     grade: Optional[str] = None
#     raceTip: Optional[str] = None



# class Temperature(BaseModel):
#     fahrenheit: Optional[float] = None
#     celsius: Optional[float] = None


# class FixtureHeader(BaseModel, DateMixin):
#     id: str
#     date: date
#     racecount: Optional[int] = None
#     temperature: Optional[Temperature] = None
#     firstposttime: Optional[datetime] = None
#     @field_validator('firstposttime', mode='before')
#     @classmethod
#     def parse_firstposttime(cls, v):
#         if isinstance(v, str):
#             return parse(v)
#         return v

# class Fixture(BaseModel):
#     header: FixtureHeader
#     track: Track = Field(default_factory=Track)
#     races: Optional[List[Race]] = []



# class Weight(BaseModel):
#     value: Optional[str] = None
#     overweight: Optional[str] = None
#     unit: Optional[str] = None


# class Jockey(BaseModel):
#     jockey_id: Optional[str] = None # id
#     jockey_name: Optional[str] = None # name

# class Withdrawn(BaseModel):
#     market: Optional[int] = None
#     timestamp: Optional[datetime] = None
#     denominator: Optional[str] = None
#     numerator: Optional[str] = None


# class FinalPosition(BaseModel):
#     position: Optional[str] = None
#     deadHeat: Optional[str] = None
#     disqualified: Optional[bool] = None
#     amendedPosition: Optional[str] = None






class Horse(BaseModel):
    horse_id: str
    externalId: str
    name: str
    gender: str
    breed: str
    foaling_date: date
    foaling_country: str
    color: str
    breeder: str
    horse_id_sire: str
    horse_id_dam: str
    horse_id_sire_dam: str
    horse_id_sire_sire: str
    horse_id_dam_sire: str
    horse_id_dam_dam: str




class PriceHistory(BaseModel):
    timestamp: Optional[datetime] = None
    numerator: Optional[str] = None
    denominator: Optional[str] = None
    price: Optional[float] = None
    market: Optional[str] = None
    @field_validator('price', mode='after')
    @classmethod
    def calculate_show_price(cls, v, info):
        if v and v.numerator and v.denominator:
            return float(v.numerator) / float(v.denominator)


class Entry(BaseModel):
    entry_id: str
    programNumber: str
    startNumber: Optional[str] = None
    startPosition: Optional[str] = None
    coupledIndicator: Optional[int] = None
    decoupledNumber: Optional[str] = None
    scratch_indicator: Optional[str] = None
    horse_id: Optional[str] = None
    age: Optional[int] = None
    saddleclothcolor: Optional[str] = None
    status_id: Optional[int] = None # status
    weight: Optional[str] = None
    weight_unit: Optional[str] = None
    breeder: Optional[str] = None
    owner_id: Optional[str] = None # id
    owner_name: Optional[str] = None # name
    trainer_id: Optional[str] = None # id
    trainer_name: Optional[str] = None # name
    jockey_id: Optional[str] = None # id
    jockey_name: Optional[str] = None # name
    position: Optional[str] = None
    deadHeat: Optional[str] = None
    disqualified: Optional[bool] = None
    amendedPosition: Optional[str] = None
    starting_price_nominator: Optional[str] = None
    starting_price_denominator: Optional[str] = None
    starting_price: Optional[float] = None
    runnerTip: Optional[str] = None
    price_history: Optional[List[PriceHistory]] = []
    def model_post_init(self, __context: Any) -> None:
        if self.starting_price_nominator and self.starting_price_denominator:
            try:
                self.starting_price = float(self.starting_price_nominator) / float(self.starting_price_denominator)
            except (ValueError, TypeError):
                self.starting_price = None
        else:
            self.starting_price = None



class StatusHistory(BaseModel):
    status: Optional[str] = None
    timestamp: Optional[datetime] = None


class Race(BaseModel):
    race_id: str # id
    type: Optional[str] = None
    race_number: str # number
    runnercount: Optional[int] = None
    posttime: Optional[datetime] = None
    estimatedPosttime: Optional[datetime] = None
    offTime: Optional[datetime] = None
    weather: Optional[str] = None
    going: Optional[str] = None
    race_name: Optional[str] = None # name
    status: Optional[str] = None
    timezoneOffset: Optional[int] = None
    tracksurface: Optional[str] = None
    overround: Optional[str] = None
    overround_selection: Optional[str] = None
    comment: Optional[str] = None
    distance: Optional[str] = None
    distance_unit: Optional[str] = None
    distance_text: Optional[str] = None
    breed: Optional[str] = None
    racetype_type: Optional[str] = None
    racetype_subtype: Optional[str] = None
    racetype_description: Optional[str] = None
    agerestriction: Optional[str] = None
    agerestriction_description: Optional[str] = None
    purse: Optional[str] = None
    purse_unit: Optional[str] = None
    grade: Optional[str] = None
    raceTip: Optional[str] = None
    statusHistory: Optional[List[StatusHistory]] = []
    entries: Optional[List[Entry]] = []


class Track(BaseModel):
    track_id: str # id
    track_name: Optional[str] = None # name
    countryid: Optional[str] = None
    countryName: Optional[str] = None
    timezone: Optional[str] = None
    code: Optional[str] = None
    trackType: Optional[str] = None


class Fixture(BaseModel):
    fixture_id: str # id
    fixture_date: date # date
    firstposttime: Optional[datetime] = None
    racecount: Optional[int] = None
    temperature_fahrenheit: Optional[float] = None
    temperature_celsius: Optional[float] = None
    track: Track = Field(default_factory=Track)
    races: Optional[List[Race]] = []


