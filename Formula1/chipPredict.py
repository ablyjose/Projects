from urllib.request import urlopen
import json
import pandas as pd
# import fastf1 as ff1

# ff1.Cache.enable_cache('Formula1/cache')

# Ergast API is deprecated, using manual get_driver_standings function instead
def get_driver_standings():
    driver_call = urlopen(f"https://api.openf1.org/v1/drivers?session_key=9693")
    driver_data = json.loads(driver_call.read().decode('utf-8'))
    drivers = pd.DataFrame(driver_data)
    standings = pd.DataFrame({
        'DriverNumber': drivers['driver_number'],
        'Driver': drivers['full_name'],
        'Points': 0.0,
        'Team': drivers['team_name'],
    })
    standings.index = range(1, len(standings) + 1)
    
    schedule_call = urlopen(f"https://api.openf1.org/v1/sessions?date_start>=2025-01-01&session_type=Race")
    data = json.loads(schedule_call.read().decode('utf-8'))
    schedule = pd.DataFrame(data)
    session_keys = schedule['session_key'].tolist()

    for key in session_keys:
        session_call = urlopen(f"https://api.openf1.org/v1/session_result?session_key={key}")
        session_data = json.loads(session_call.read().decode('utf-8'))
        results = pd.DataFrame(session_data)
        
        for index, row in results.iterrows():
            driver_number = row['driver_number']
            points = row['points']
            
            if driver_number in standings['DriverNumber'].values:
                standings.loc[standings['DriverNumber'] == driver_number, 'Points'] += points
            else:
                new_driver_call = urlopen(f"https://api.openf1.org/v1/drivers?driver_number={driver_number}&session_key={key}")
                new_data = json.loads(new_driver_call.read().decode('utf-8'))
                new_driver = pd.DataFrame(new_data)

                new_row = pd.DataFrame({
                    'DriverNumber': new_driver['driver_number'],
                    'Driver': new_driver['full_name'],
                    'Points': points,
                    'Team': new_driver['team_name']
                })
                standings = pd.concat([standings, new_row], ignore_index=True)

    updated_standings = standings.sort_values(by='Points', ascending=False).reset_index(drop=True)
    updated_standings.index = range(1, len(updated_standings) + 1)
    updated_standings.to_csv('Formula1/standings.csv', index_label='Position')
    return updated_standings

print(get_driver_standings())