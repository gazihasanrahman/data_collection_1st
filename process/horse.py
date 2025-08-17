import traceback
from dateutil.parser import parse
from utils.logger import logger_1st


def process_horse_data(horse_data: dict) -> dict | None:
    '''
    process horse data received from pull method, which we pull from 1st's API.
    '''
    
    if not horse_data:
        return None
    
    try:
        horse_id = horse_data.get('horse_id')
        if not horse_id:
            logger_1st.error(f'process_horse_data(): horse_id is missing')
            return None

        external_id = horse_data.get('externalId')
        horse_name = horse_data.get('name')
        gender = horse_data.get('gender', {}).get('details')
        breed = horse_data.get('breed', {}).get('details')
        foaling_date_str = horse_data.get('foaling', {}).get('date')
        foaling_date = parse(foaling_date_str).date() if foaling_date_str else None
        foaling_country = horse_data.get('foaling', {}).get('country')
        color = horse_data.get('color', {}).get('details')
        breeder = horse_data.get('breeder')
        pedigree = horse_data.get('pedigree', [])

        # Initialize pedigree variables
        horse_id_sire = None
        horse_id_dam = None
        horse_id_sire_dam = None
        horse_id_sire_sire = None
        horse_id_dam_sire = None
        horse_id_dam_dam = None

        for pedigree_item in pedigree:
            pedigree_id = pedigree_item.get('id')
            pedigree_type = pedigree_item.get('type')
            if pedigree_type == 'Sire':
                horse_id_sire = pedigree_id
            elif pedigree_type == 'Dam':
                horse_id_dam = pedigree_id
            elif pedigree_type == 'SireDam':
                horse_id_sire_dam = pedigree_id
            elif pedigree_type == 'SireSire':
                horse_id_sire_sire = pedigree_id
            elif pedigree_type == 'DamSire':
                horse_id_dam_sire = pedigree_id
            elif pedigree_type == 'DamDam':
                horse_id_dam_dam = pedigree_id

        return {
            'horse_id': horse_id,
            'external_id': external_id,
            'horse_name': horse_name,
            'gender': gender,
            'breed': breed,
            'foaling_date': foaling_date,
            'foaling_country': foaling_country,
            'color': color,
            'breeder': breeder,
            'horse_id_sire': horse_id_sire,
            'horse_id_dam': horse_id_dam,
            'horse_id_sire_dam': horse_id_sire_dam,
            'horse_id_sire_sire': horse_id_sire_sire,
            'horse_id_dam_sire': horse_id_dam_sire,
            'horse_id_dam_dam': horse_id_dam_dam,
        }

    except Exception as e:
        logger_1st.error(f'process_horse_data(): {e}')
        logger_1st.error(traceback.format_exc())
        return None

