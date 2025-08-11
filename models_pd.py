import json
import glob
import pandas as pd
from pydantic import BaseModel, field_validator, Field
from datetime import datetime, timedelta, date
from dateutil.parser import parse
from typing import List, Optional, Union, Dict, Any


class Horse(BaseModel):
    horse_id: str
    externalId: Optional[str] = None
    name: str
    gender: Optional[str] = None
    breed: Optional[str] = None
    foaling_date: Optional[date] = None
    foaling_country: Optional[str] = None
    color: Optional[str] = None
    breeder: Optional[str] = None
    horse_id_sire: Optional[str] = None
    horse_id_dam: Optional[str] = None
    horse_id_sire_dam: Optional[str] = None
    horse_id_sire_sire: Optional[str] = None
    horse_id_dam_sire: Optional[str] = None
    horse_id_dam_dam: Optional[str] = None

class PriceHistory(BaseModel):
    timestamp: Optional[datetime] = None
    numerator: Optional[str] = None
    denominator: Optional[str] = None
    price: Optional[float] = None
    market: Optional[str] = None
    
    @field_validator('timestamp', mode='before')
    @classmethod
    def parse_timestamp(cls, v):
        if isinstance(v, str):
            try:
                return parse(v)
            except:
                return None
        return v
    
    @field_validator('price', mode='after')
    @classmethod
    def calculate_price(cls, v, info):
        if v is None and info.data.get('numerator') and info.data.get('denominator'):
            try:
                return float(info.data['numerator']) / float(info.data['denominator'])
            except (ValueError, TypeError):
                return None
        return v


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
    
    @field_validator('timestamp', mode='before')
    @classmethod
    def parse_timestamp(cls, v):
        if isinstance(v, str):
            try:
                return parse(v)
            except:
                return None
        return v


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
    
    @field_validator('posttime', 'estimatedPosttime', 'offTime', mode='before')
    @classmethod
    def parse_datetime_fields(cls, v):
        if isinstance(v, str):
            try:
                return parse(v)
            except:
                return None
        return v


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
    
    @field_validator('fixture_date', mode='before')
    @classmethod
    def parse_date(cls, v):
        if isinstance(v, str):
            try:
                return datetime.strptime(v, '%Y-%m-%d').date()
            except:
                return None
        return v
    
    @field_validator('firstposttime', mode='before')
    @classmethod
    def parse_firstposttime(cls, v):
        if isinstance(v, str):
            try:
                return parse(v)
            except:
                return None
        return v


