import json
from process.race import process_race_data


# load the file
file_location = '/home/gazi/Desktop/downloads/1754940229048.json'
with open(file_location, 'r') as f:
    race_data = json.load(f)

race_result = process_race_data(race_data)
fixtures = race_result['fixtures']
race_status_history_dict = race_result['race_status_history_dict']
price_history_dict = race_result['price_history_dict']

print(race_status_history_dict)
print(price_history_dict)

print(race_result)

# for fixture in fixtures:
#     # print(f'fixture_id: {fixture["fixture_id"]}')
#     # print(f'fixture_date: {fixture["fixture_date"]}')
#     # print(f'first_post_time: {fixture["first_post_time"]}')
#     # print(f'race_count: {fixture["race_count"]}')
#     # print(f'temperature_fahrenheit: {fixture["temperature_fahrenheit"]}')
#     # print(f'temperature_celsius: {fixture["temperature_celsius"]}')
#     # print(f'track_id: {fixture["track_id"]}')
#     # print(f'tpd_meeting_id: {fixture["tpd_meeting_id"]}')
#     # print('-'*100)
#     for race in fixture["race_data"]:
#         # print(f'race_id: {race["race_id"]}')
#         # print(f'race_number: {race["race_number"]}')
#         # print(f'runner_count: {race["runner_count"]}')
#         # print(f'post_time: {race["post_time"]}')
#         # print(f'estimated_post_time: {race["estimated_post_time"]}')
#         # print(f'off_time: {race["off_time"]}')
#         # print(f'weather: {race["weather"]}')
#         # print(f'going: {race["going"]}')
#         # print(f'race_name: {race["race_name"]}')
#         # print(f'race_status: {race["race_status"]}')
#         # print(f'overround: {race["overround"]}')
#         # print(f'overround_selection: {race["overround_selection"]}')
#         # print(f'race_result: {race["race_result"]}')
#         # print(f'surface: {race["surface"]}')
#         # print(f'tpd_race_id: {race["tpd_race_id"]}')
#         # print('-'*100)

#         for race_status_history in race["race_status_history_data"]:
#             print(f'race_status_id: {race_status_history["race_status_id"]}')
#             print(f'race_id: {race_status_history["race_id"]}')
#             print(f'status: {race_status_history["status"]}')
#             print(f'timestamp: {race_status_history["timestamp"]}')
#             print('-'*100)

#         for entry in race["entry_data"]:
#             # print(f'entry_id: {entry["entry_id"]}')
#             # print(f'start_number: {entry["start_number"]}')
#             # print(f'entry_program_number: {entry["entry_program_number"]}')
#             # print(f'start_position: {entry["start_position"]}')
#             # print(f'coupled_indicator: {entry["coupled_indicator"]}')
#             # print(f'decoupled_number: {entry["decoupled_number"]}')
#             # print(f'horse_id: {entry["horse_id"]}')
#             # print(f'horse_name: {entry["horse_name"]}')
#             # print(f'entry_status: {entry["entry_status"]}')
#             # print(f'weight_value: {entry["weight_value"]}')
#             # print(f'weight_unit: {entry["weight_unit"]}')
#             # print(f'jockey_id: {entry["jockey_id"]}')
#             # print(f'jockey_name: {entry["jockey_name"]}')
#             # print(f'starting_price_fraction: {entry["starting_price_fraction"]}')
#             # print(f'starting_price_percentage: {entry["starting_price_percentage"]}')
#             # print(f'fav_pos: {entry["fav_pos"]}')
#             # print(f'fav_joint: {entry["fav_joint"]}')
#             # print(f'final_position: {entry["final_position"]}')
#             # print(f'dead_heat: {entry["dead_heat"]}')
#             # print(f'disqualified: {entry["disqualified"]}')
#             # print(f'amended_position: {entry["amended_position"]}')
#             # print(f'tpd_runner_id: {entry["tpd_runner_id"]}')
#             # print('-'*100)
#             for historical_price in entry["historical_price_data"]:
#                 print(f'price_id: {historical_price["price_id"]}')
#                 print(f'entry_id: {historical_price["entry_id"]}')
#                 print(f'timestamp: {historical_price["timestamp"]}')
#                 print(f'price_fraction: {historical_price["price_fraction"]}')
#                 print(f'price_percentage: {historical_price["price_percentage"]}')
#                 print(f'market: {historical_price["market"]}')
#                 print('-'*100)





