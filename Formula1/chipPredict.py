import pandas as pd
import fastf1 as ff1
from driverStandings import get_driver_standings

ff1.Cache.enable_cache('Formula1/cache')

# Ergast API is deprecated, using manual get_driver_standings function instead
print(get_driver_standings())