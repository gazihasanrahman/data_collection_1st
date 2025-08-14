import json
from process.fixture import process_fixture_data
from upload.fixture import upload_fixture_data
from first import FirstAPI
from datetime import date










if __name__ == '__main__':
    # file_path = '/home/gazi/main_dir/data_collection_1st/downloads/sample_fofixtures_1.json'
    # with open(file_path, 'r') as file:
    #     fixture_data = json.load(file)
    
    first_api = FirstAPI()
    fixture_data = first_api.get_fofixtures(date=date(2025, 8, 14))

    fixture_result = process_fixture_data(fixture_data)
    fixtures = fixture_result['fixtures']
    jockey_dict = fixture_result['jockey_dict']
    trainer_dict = fixture_result['trainer_dict']
    owner_dict = fixture_result['owner_dict']

    for fixture in fixtures:
        # print(fixture['fixture_id'])
        # print(len(fixture['race_data']))
        upload_fixture_data(fixture, overwrite=True)