import fastf1 as ff1
from fastf1 import plotting
from fastf1 import utils
from fastf1.core import Laps
from fastf1.api import race_control_messages

import pandas as pd

ff1.Cache.enable_cache('Formula1/cache')

driver = "NOR"

year, gp, session = 2025, "Hungary", 'FP1' 

p1 = ff1.get_session(year, gp, session)
p1.load(weather=True, laps=True, telemetry=False, messages=False)

session = "FP2"
p2 = ff1.get_session(year, gp, session)
p2.load(weather=True, laps=True, telemetry=False, messages=False)

print(p1.laps.pick_drivers(driver).sort_values(by='Time')[['Time', 'LapTime', 'LapNumber', 'Stint', 'Compound', 'TyreLife']])
print("Average Track Temp:", p1.weather_data['TrackTemp'].mean())
print("Average Air Temp:", p1.weather_data['AirTemp'].mean())
print()

print(p2.laps.pick_drivers(driver).sort_values(by='Time')[['Time', 'LapTime', 'LapNumber', 'Stint', 'Compound', 'TyreLife']])
print("Average Track Temp:", p2.weather_data['TrackTemp'].mean())
print("Average Air Temp:", p2.weather_data['AirTemp'].mean())