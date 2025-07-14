import json
import glob
import pandas as pd
from pydantic import BaseModel, field_validator, Field
from datetime import datetime, timedelta, date
from dateutil.parser import parse
from typing import List, Optional, Union, Dict, Any


# Mixin classes for datetime parsing
class TimestampMixin:
    @field_validator('timestamp', mode='before')
    @classmethod
    def parse_timestamp(cls, v):
        if isinstance(v, str):
            return parse(v)
        return v

class DateTimeFieldsMixin:
    @field_validator('posttime', 'estimatedPosttime', 'offTime', mode='before')
    @classmethod
    def parse_datetime_fields(cls, v):
        if isinstance(v, str):
            return parse(v)
        return v

class DateMixin:
    @field_validator('date', mode='before')
    @classmethod
    def parse_date(cls, v):
        if isinstance(v, str):
            return datetime.strptime(v, '%Y-%m-%d').date()
        return v


# Temperature models
class Temperature(BaseModel):
    fahrenheit: Optional[float] = None
    celsius: Optional[float] = None


# Fixture header models
class FixtureHeader(BaseModel, DateMixin):
    id: str
    date: date
    racecount: Optional[int] = None
    temperature: Optional[Temperature] = None
    firstposttime: Optional[datetime] = None
    
    @field_validator('firstposttime', mode='before')
    @classmethod
    def parse_firstposttime(cls, v):
        if isinstance(v, str):
            return parse(v)
        return v


# Track model
class Track(BaseModel):
    id: str
    name: Optional[str] = None
    countryid: Optional[str] = None
    countryName: Optional[str] = None
    timezone: Optional[str] = None
    isdst: Optional[bool] = None
    timezoneOffset: Optional[int] = None
    code: Optional[str] = None
    videocode: Optional[str] = None
    trackType: Optional[str] = None


# Status history model
class StatusHistory(BaseModel, TimestampMixin):
    status: Optional[str] = None
    timestamp: Optional[datetime] = None


# Track surface model
class TrackSurface(BaseModel):
    value: Optional[str] = None


# Equipment model
class Equipment(BaseModel):
    code: Optional[str] = None
    description: Optional[str] = None


# Weight model
class Weight(BaseModel):
    value: Optional[str] = None
    overweight: Optional[str] = None
    unit: Optional[str] = None


# Jockey model
class Jockey(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    oldJockeyID: Optional[str] = None
    oldJockeyName: Optional[str] = None


# Show price model
class ShowPrice(BaseModel, TimestampMixin):
    timestamp: Optional[datetime] = None
    numerator: Optional[str] = None
    denominator: Optional[str] = None
    # calculate the show price as a float
    price: Optional[float] = None
    @field_validator('price', mode='after')
    @classmethod
    def calculate_show_price(cls, v, info):
        if v and v.numerator and v.denominator:
            return float(v.numerator) / float(v.denominator)
    market: Optional[str] = None





class Withdrawn(BaseModel, TimestampMixin):
    market: Optional[int] = None
    timestamp: Optional[datetime] = None
    denominator: Optional[str] = None
    numerator: Optional[str] = None


class FinalPosition(BaseModel):
    position: Optional[str] = None
    deadHeat: Optional[str] = None
    disqualified: Optional[bool] = None
    amendedPosition: Optional[str] = None


class Entry(BaseModel):
    id: str
    startNumber: str
    programNumber: Optional[str] = None
    startPosition: Optional[str] = None
    coupledIndicator: Optional[int] = None
    decoupledNumber: Optional[str] = None
    horse_id: Optional[str] = None
    name: Optional[str] = None
    status: Optional[int] = None
    equipment: Equipment = Field(default_factory=Equipment)
    weight: Optional[Weight] = None
    jockey: Optional[Jockey] = None
    showPrices: Optional[List[ShowPrice]] = []
    startingPrice: Optional[Dict[Optional[str], Optional[str]]] = None
    # calculate the starting price as a float
    starting_price: Optional[float] = None

    favPos: Optional[str] = None
    favJoint: Optional[str] = None
    withdrawn: Withdrawn = Field(default_factory=Withdrawn)
    finalPosition: FinalPosition = Field(default_factory=FinalPosition)
    
    def model_post_init(self, __context: Any) -> None:
        """Calculate starting price float after model initialization"""
        if self.startingPrice and 'nominator' in self.startingPrice and 'denominator' in self.startingPrice:
            try:
                self.starting_price = float(self.startingPrice['nominator']) / float(self.startingPrice['denominator'])
            except (ValueError, TypeError):
                self.starting_price = None
        else:
            self.starting_price = None


class Distance(BaseModel):
    value: Optional[str] = None
    unit: Optional[str] = None
    publishedText: Optional[str] = None


class Purse(BaseModel):
    value: Optional[str] = None
    ranks: Optional[str] = None
    unit: Optional[str] = None


class SexRestriction(BaseModel):
    value: Optional[str] = None
    description: Optional[str] = None


class AgeRestriction(BaseModel):
    value: Optional[str] = None
    description: Optional[str] = None


class RaceType(BaseModel):
    type: Optional[str] = None
    subtype: Optional[str] = None
    description: Optional[str] = None


class Race(BaseModel, DateTimeFieldsMixin):
    id: str
    type: Optional[str] = None
    number: str
    runnercount: Optional[int] = None
    posttime: Optional[datetime] = None
    estimatedPosttime: Optional[datetime] = None
    offTime: Optional[datetime] = None
    weather: Optional[str] = None
    going: Optional[str] = None
    name: Optional[str] = None
    status: Optional[str] = None
    statusHistory: Optional[List[StatusHistory]] = []
    isdst: Optional[bool] = None
    timezoneOffset: Optional[int] = None
    tracksurface: TrackSurface = Field(default_factory=TrackSurface)
    overround: Optional[str] = None
    overround_selection: Optional[str] = None
    entries: Optional[List[Entry]] = []
    result: Optional[str] = None
    comment: Optional[str] = None
    distance: Distance = Field(default_factory=Distance)
    breed: Optional[str] = None
    racetype: RaceType = Field(default_factory=RaceType)
    sexrestriction: SexRestriction = Field(default_factory=SexRestriction)
    agerestriction: AgeRestriction = Field(default_factory=AgeRestriction)
    purse: Purse = Field(default_factory=Purse)
    grade: Optional[str] = None
    raceTip: Optional[str] = None


class Fixture(BaseModel):
    header: FixtureHeader
    track: Track = Field(default_factory=Track)
    races: Optional[List[Race]] = []

