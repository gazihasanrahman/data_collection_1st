import json
from process.fixture import process_fixture_data
from upload.fixture import upload_fixture_data
from first import FirstAPI
from datetime import date
import time









if __name__ == '__main__':
    # file_path = '/home/gazi/main_dir/data_collection_1st/downloads/sample_fofixtures_1.json'
    # with open(file_path, 'r') as file:
    #     fixture_data = json.load(file)



    date_list = [date(2025, 8, 1), date(2025, 8, 2), date(2025, 8, 3), date(2025, 8, 4), date(2025, 8, 5), 
                 date(2025, 8, 6), date(2025, 8, 7), date(2025, 8, 8), date(2025, 8, 9), date(2025, 8, 10), 
                 date(2025, 8, 11), date(2025, 8, 12), date(2025, 8, 13), date(2025, 8, 14), date(2025, 8, 15), 
                 date(2025, 8, 16), date(2025, 8, 17), date(2025, 8, 18), date(2025, 8, 19), date(2025, 8, 20)
    ]



    first_api = FirstAPI()



    for date in date_list:
        fixture_data = first_api.get_fofixtures(date=date)

        try:
            print(f'Processing {date} | items: {len(fixture_data)}')
        except Exception as e:
            print(f'Error processing {date}: {e}')
            continue

        fixture_result = process_fixture_data(fixture_data)
        fixtures = fixture_result['fixtures']
        jockey_dict = fixture_result['jockey_dict']
        trainer_dict = fixture_result['trainer_dict']
        owner_dict = fixture_result['owner_dict']

        for fixture in fixtures:
            # print(fixture['fixture_id'])
            # print(len(fixture['race_data']))
            upload_fixture_data(fixture, overwrite=True)

        time.sleep(10)
        
