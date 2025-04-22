import fastf1 as ff1
from fastf1 import plotting
from fastf1 import utils
from fastf1.core import Laps
from fastf1.api import race_control_messages

import pandas as pd

ff1.Cache.enable_cache('C:/Users/albys/PortProjects/Formula1/cache')

year, gp, session = 2024, "Brazil", 'R' 

race = ff1.get_session(year, gp, session)
race.load(messages=True)

print(race.race_control_messages[race.race_control_messages.Category == 'SafetyCar'])

