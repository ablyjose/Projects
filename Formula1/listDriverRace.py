import pandas as pd

import fastf1 as ff1
from fastf1.core import Laps

ff1.Cache.enable_cache('Formula1/cache')

year, gp, session_type = int(input("Year: ")), input("GP: "), input("Session: ")

session = ff1.get_event(year, gp).get_session(session_type)
session.load()

drivers = input("Drivers: ").upper().replace(" ", "").split(',')

for driver in drivers:
    driver_laps = session.laps.pick_drivers(driver)
    pd.set_option('display.max_rows', None) 
    # pd.set_option('display.max_columns', None)
    print(driver_laps[['Driver', 'LapTime', 'LapNumber', 'Stint', 'Compound', 'TyreLife', 'Sector1Time', 'Sector2Time', 'Sector3Time', 'SpeedI1', 'SpeedI2', 'SpeedFL', 'SpeedST', 'Deleted', 'DeletedReason']]\
          .sort_values(by='LapNumber')\
            .reset_index(drop=True))
    print("--------------------------------------------------------------------------------------------------------------------------------\n")
    

# print(final_laps.columns)