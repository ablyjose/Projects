import fastf1 as ff1
from fastf1 import plotting
from fastf1 import utils
from fastf1.core import Laps

from matplotlib import pyplot as plt
# from matplotlib.pyplot import figure

import numpy as np
import pandas as pd

ff1.Cache.enable_cache('Formula1/cache')

year, gp, session_name = 2025, "Brazil", 'R'

session = ff1.get_session(year, gp, session_name)
session.load(messages=False, weather=False)

# pick the first four drivers in the order they appear in the loaded laps
drivers = ['NOR', 'PIA', 'VER'] # hard coded drivers in due to inconsistent order in which drivers appear in laps data
linestyles = ['-', ':']
linestyle_mapping = {driver: linestyles[i % len(linestyles)] for i, driver in enumerate(drivers)}
race_sims = list()

for drv in drivers:
    racepacelaps = session.laps.pick_drivers(drv).pick_wo_box().pick_quicklaps()
    race_sims.append(racepacelaps)

    driver_color = '#' + session.get_driver(drv)['TeamColor']
    driver_linestyle = linestyle_mapping[drv]
    driver_style = {'color': driver_color, 'linestyle': driver_linestyle}
    plt.plot(racepacelaps['LapNumber'], racepacelaps['LapTime'].dt.total_seconds(), **driver_style, label=drv)
    
plt.xlabel('Lap Number')
plt.ylabel('Lap Time (s)')
plt.title(f'{year} {gp} GP Race Pace Simulation')
plt.legend(title='Driver')

plt.show()
# race_simulation_laps = Laps(pd.concat(race_sims)) \
#     .sort_values(by=['Driver', 'LapNumber']) \
#     .reset_index(drop=True)

# print(race_simulation_laps[['Driver', 'LapTime', 'LapNumber', 'Stint', 'Compound', 'TyreLife']])