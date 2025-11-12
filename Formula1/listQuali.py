import pandas as pd

import fastf1 as ff1
from fastf1.core import Laps

ff1.Cache.enable_cache('Formula1/cache')

year, gp, session = 2025, "Saudi Arabia", 'Q'

quali = ff1.get_session(year, gp, session)
quali.load(weather=False, messages=False, telemetry=False)

drivers = pd.unique(quali.laps['Driver'])

q1_results = list()
q2_results = list()
q3_results = list()

dnf_time = pd.Timedelta(minutes=4)

for drv in drivers:
    q1, q2, q3 = quali.laps.pick_drivers(drv).split_qualifying_sessions()

    fastest_q1 = q1.pick_fastest()
    if pd.isna(fastest_q1['LapTime']):
            fastest_q1['LapTime'] = dnf_time
            dnf_time += pd.Timedelta(minutes=1)
            fastest_q1['Driver'] = drv
    q1_results.append(fastest_q1)
    if q2 is not None:
        fastest_q2 = q2.pick_fastest()
        if pd.isna(fastest_q2['LapTime']):
            fastest_q2['LapTime'] = dnf_time
            dnf_time += pd.Timedelta(minutes=1)
            fastest_q2['Driver'] = drv
        q2_results.append(fastest_q2)
    if q3 is not None:
        fastest_q3 = q3.pick_fastest()
        if pd.isna(fastest_q3['LapTime']):
            fastest_q3['LapTime'] = dnf_time
            dnf_time += pd.Timedelta(minutes=1)
            fastest_q3['Driver'] = drv
        q3_results.append(fastest_q3)

q1_order = Laps(q1_results) \
    .sort_values(by='LapTime') \
    .reset_index(drop=True)
q1_pole = q1_order.pick_fastest()
q1_order['DeltaToPole'] = q1_order['LapTime'] - q1_pole['LapTime']
for laptime in q1_order['LapTime']:
    if laptime >= q1_order.iloc[0]['LapTime'] * 1.07:
        q1_order.loc[q1_order['LapTime'] >= q1_order['LapTime'].iloc[0] * 1.07, 'LapTime'] = "DNF"
        q1_order.loc[q1_order['LapTime'] == "DNF", 'DeltaToPole'] = "N/A"

q2_order = Laps(q2_results) \
    .sort_values(by='LapTime') \
    .reset_index(drop=True)
q2_pole = q2_order.pick_fastest()
q2_order['DeltaToPole'] = q2_order['LapTime'] - q2_pole['LapTime']
for laptime in q2_order['LapTime']:
    if laptime >= q2_order.iloc[0]['LapTime'] * 1.07:
        q2_order.loc[q2_order['LapTime'] >= q2_order['LapTime'].iloc[0] * 1.07, 'LapTime'] = "DNF"
        q2_order.loc[q2_order['LapTime'] == "DNF", 'DeltaToPole'] = "N/A"

q3_order = Laps(q3_results) \
    .sort_values(by='LapTime') \
    .reset_index(drop=True)
q3_pole = q3_order.pick_fastest()
q3_order['DeltaToPole'] = (q3_order['LapTime'] - q3_pole['LapTime'])
for laptime in q3_order['LapTime']:
    if laptime >= q3_order.iloc[0]['LapTime'] * 1.07:
        q3_order.loc[q3_order['LapTime'] >= q3_order['LapTime'].iloc[0] * 1.07, 'LapTime'] = "DNF"
        q3_order.loc[q3_order['LapTime'] == "DNF", 'DeltaToPole'] = "N/A"

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