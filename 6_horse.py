import json
import glob
import pandas as pd
from sqlalchemy import text
from pydantic import BaseModel, field_validator
from datetime import datetime, timedelta, date
from dateutil.parser import parse
from typing import List, Optional, Union, Dict, Any
from models_pd import Fixture, Race, Entry, Horse
from database.models import FirstHorse
from database.sql import session_scope
import models_pd as etl
from first import FirstAPI

def parse_horse(data: Dict[str, Any]) -> etl.Horse:

    horse_id_sire = None
    horse_id_dam = None
    horse_id_sire_dam = None
    horse_id_sire_sire = None
    horse_id_dam_sire = None
    horse_id_dam_dam = None
    
    for pedigree in data.get('pedigree',[]):
        if pedigree.get('type') == 'Sire':
            horse_id_sire = pedigree.get('id')
        elif pedigree.get('type') == 'Dam':
            horse_id_dam = pedigree.get('id')
        elif pedigree.get('type') == 'SireDam':
            horse_id_sire_dam = pedigree.get('id')
        elif pedigree.get('type') == 'SireSire':
            horse_id_sire_sire = pedigree.get('id')
        elif pedigree.get('type') == 'DamSire':
            horse_id_dam_sire = pedigree.get('id')
        elif pedigree.get('type') == 'DamDam':
            horse_id_dam_dam = pedigree.get('id')

    return etl.Horse(
        horse_id=data.get('horse_id'),
        externalId=data.get('externalId'),
        name=data.get('name'),
        gender=data.get('gender',{}).get('details'),
        breed=data.get('breed',{}).get('details'),
        foaling_date=data.get('foaling',{}).get('date'),
        foaling_country=data.get('foaling',{}).get('country'),
        color=data.get('color',{}).get('details'),
        breeder=data.get('breeder'),
        horse_id_sire=horse_id_sire,
        horse_id_dam=horse_id_dam,
        horse_id_sire_dam=horse_id_sire_dam,
        horse_id_sire_sire=horse_id_sire_sire,
        horse_id_dam_sire=horse_id_dam_sire,
        horse_id_dam_dam=horse_id_dam_dam,
    )


# with open('downloads/sample_horses_1.json', 'r') as f:
#     data = json.load(f)

with session_scope() as session:
    query = text("select distinct(horse_id) from first.first_entry")
    result = session.execute(query)
    horse_ids = result.fetchall()
    list_of_horse_ids = [horse_id[0] for horse_id in horse_ids]

# print(list_of_horse_ids)


# horse_id = list_of_horse_ids[0]


first = FirstAPI()



for horse_id in list_of_horse_ids:
    try:
        data = first.get_horses(horse_id=horse_id)
        horse = parse_horse(data)


        with session_scope() as session:

            # check if horse already exists
            existing_horse = session.query(FirstHorse).filter(FirstHorse.horse_id == horse.horse_id).first()
            if not existing_horse:
                first_horse = FirstHorse(
                    horse_id=horse.horse_id,
                    external_id=horse.externalId,
                    name=horse.name,
                    gender=horse.gender,
                    breed=horse.breed,
                    foaling_date=horse.foaling_date,
                    foaling_country=horse.foaling_country,
                    color=horse.color,
                    breeder=horse.breeder,
                    horse_id_sire=horse.horse_id_sire,
                    horse_id_dam=horse.horse_id_dam,
                    horse_id_sire_dam=horse.horse_id_sire_dam,
                    horse_id_sire_sire=horse.horse_id_sire_sire,
                    horse_id_dam_sire=horse.horse_id_dam_sire,
                    horse_id_dam_dam=horse.horse_id_dam_dam,
                )
                session.add(first_horse)
                session.commit()
                print(f"Horse {horse.horse_id} added to the database")
            else:
                print(f"Horse {horse.horse_id} already exists in the database")
    except Exception as e:
        print(f"Error processing horse {horse_id}: {e}")
        continue





