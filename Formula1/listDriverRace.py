import pandas as pd

import fastf1 as ff1
from fastf1.core import Laps

ff1.Cache.enable_cache('Formula1/cache')

year, gp, session = 2025, "Japan", 'R'

race = ff1.get_session(year, gp, session)
race.load()

drivers_laps = race.laps.pick_drivers(['NOR', 'PIA']).pick_laps(45)

print(drivers_laps.T)