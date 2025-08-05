import pandas as pd

import fastf1 as ff1
from fastf1.core import Laps

ff1.Cache.enable_cache('Formula1/cache')

year, gp, session = 2025, "Hungary", 'Q'

quali = ff1.get_session(year, gp, session)
quali.load()

drivers = ['LEC', 'HAM']
list_final_laps = list()

for driver in drivers:
    driver_laps = quali.laps.pick_drivers(driver).pick_fastest()    
    list_final_laps.append(driver_laps)

final_laps = Laps(list_final_laps) \
    .sort_values(by=['TyreLife']) \
    .reset_index(drop=True)

# print(final_laps.columns)
print(final_laps[['Driver', 'LapTime', 'LapNumber', 'Stint', 'Compound', 'TyreLife', 'SpeedI1', 'SpeedI2', 'SpeedFL', 'SpeedST']])