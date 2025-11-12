import pandas as pd

import fastf1 as ff1
from fastf1.core import Laps

ff1.Cache.enable_cache('Formula1/cache')

year, gp, type = 2025, "Belgium", 'R'

session = ff1.get_session(year, gp, type)
session.load()

drivers = ['NOR', 'PIA']

for driver in drivers:
    driver_laps = session.laps.pick_drivers(driver)
    pd.set_option('display.max_rows', None) 
    # pd.set_option('display.max_columns', None)
    print(driver_laps[['Driver', 'LapTime', 'LapNumber', 'Stint', 'Compound', 'TyreLife', 'Sector1Time', 'Sector2Time', 'Sector3Time', 'SpeedI1', 'SpeedI2', 'SpeedFL', 'SpeedST', 'Deleted', 'DeletedReason']]\
          .sort_values(by='LapNumber')\
            .reset_index(drop=True))
    print("--------------------------------------------------------------------------------------------------------------------------------\n")
    

# print(final_laps.columns)