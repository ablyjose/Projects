import fastf1 as ff1
from fastf1 import plotting
from fastf1 import utils
from fastf1.core import Laps

# from matplotlib import pyplot as plt
# from matplotlib.pyplot import figure

import numpy as np
import pandas as pd

ff1.Cache.enable_cache('Formula1/cache')

year, gp, session = 2024, "Austria", 'FP2'

practice2 = ff1.get_session(year, gp, session)
practice2.load()

drivers = ['RUS', 'ANT']
race_sims = list()

for drv in drivers:
    racepacelaps = practice2.laps.pick_drivers(drv).pick_quicklaps(1.1)
    # fastest_race = racepacelaps.pick_fastest()
    race_sims.append(racepacelaps)
    
race_simulation_laps = Laps(pd.concat(race_sims)) \
    .sort_values(by=['Driver', 'LapNumber']) \
    .reset_index(drop=True)

# lead_racelaps = practice2.laps.pick_drivers(['HAM', 'RUS', 'LEC', 'SAI', 'NOR', 'HUL', 'VER']).pick_quicklaps().pick_compounds("MEDIUM")
pd.set_option('display.max_rows', None)

# nor_racelaps = practice2.laps.pick_drivers('NOR').pick_quicklaps()
# ver_racelaps = practice2.laps.pick_drivers('VER').pick_quicklaps()
# ham_racelaps = practice2.laps.pick_drivers('HAM').pick_quicklaps()
# rus_racelaps = practice2.laps.pick_drivers('RUS').pick_quicklaps()
# lec_racelaps = practice2.laps.pick_drivers('LEC').pick_quicklaps()
# sai_racelaps = practice2.laps.pick_drivers('SAI').pick_quicklaps()

# print(lead_racelaps[['Driver', 'LapTime', 'LapNumber', 'Stint', 'Compound', 'TyreLife']])
print(race_simulation_laps[['Driver', 'LapTime', 'LapNumber', 'Stint', 'Compound', 'TyreLife']])