import pandas as pd

import fastf1 as ff1
from fastf1.core import Laps

ff1.Cache.enable_cache('Formula1/cache')

year, gp, session = 2025, "Jeddah", 'Q'

quali = ff1.get_session(year, gp, session)
quali.load()

drivers = pd.unique(quali.laps['Driver'])

q1_results = list()
q2_results = list()
q3_results = list()

for drv in drivers:
    q1, q2, q3 = quali.laps.pick_drivers(drv).split_qualifying_sessions()

    fastest_q1 = q1.pick_fastest()
    q1_results.append(fastest_q1)
    if q2 is not None:
        fastest_q2 = q2.pick_fastest()
        q2_results.append(fastest_q2)
    if q3 is not None:
        fastest_q3 = q3.pick_fastest()
        # if drv == "HAM":
        #     fastest_q3['LapTime'] -= pd.offsets.Milli(58) # counteracts faulty pick_fastest() function in Japan '25
        q3_results.append(fastest_q3)

q1_order = Laps(q1_results) \
    .sort_values(by='LapTime') \
    .reset_index(drop=True)

q1_pole = q1_order.pick_fastest()
q1_order['DeltaToPole'] = q1_order['LapTime'] - q1_pole['LapTime']

q2_order = Laps(q2_results) \
    .sort_values(by='LapTime') \
    .reset_index(drop=True)
q2_pole = q2_order.pick_fastest()
q2_order['DeltaToPole'] = q2_order['LapTime'] - q2_pole['LapTime']

q3_order = Laps(q3_results) \
    .sort_values(by='LapTime') \
    .reset_index(drop=True)
q3_pole = q3_order.pick_fastest()
q3_order['DeltaToPole'] = (q3_order['LapTime'] - q3_pole['LapTime'])

q1_order.index += 1
q2_order.index += 1
q3_order.index += 1

print("Q1 Results")
print(q1_order[['Driver', 'LapTime', 'DeltaToPole']])
print("--------------------------------\n")

print("Q2 Results")
print(q2_order[['Driver', 'LapTime', 'DeltaToPole']])
print("--------------------------------\n")

print("Q3 Results")
print(q3_order[['Driver', 'LapTime', 'DeltaToPole']])
print("--------------------------------\n")