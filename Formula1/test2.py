import fastf1 as ff1
from fastf1 import plotting
from fastf1 import utils
from fastf1.core import Laps

from matplotlib import pyplot as plt
from matplotlib.pyplot import figure

import numpy as np
import pandas as pd

ff1.Cache.enable_cache('Formula1/cache')

year, gp, session_name = 2025, "Hungary", 'R' 

session = ff1.get_event(year, gp).get_session(session_name)
session.load(weather=False)

driver_1, driver_2 = 'NOR', 'PIA'

# Used for qualifying sessions
# q1_driver_1, q2_driver_1, q3_driver1 = session.laps.pick_drivers(driver_1).split_qualifying_sessions()
# q1_driver_2, q2_driver_2, q3_driver2 = session.laps.pick_drivers(driver_2).split_qualifying_sessions()
# 
# driver_1_laps = q3_driver1.laps.pick_drivers(driver_1).pick_fastest()
# driver_2_laps = q3_driver2.laps.pick_drivers(driver_2).pick_fastest()

# Used for race sessions
driver_1_laps = session.laps.pick_drivers(driver_1)
driver_2_laps = session.laps.pick_drivers(driver_2)

fastest_driver_1 = driver_1_laps.pick_laps(range(67, 70))
fastest_driver_2 = driver_2_laps.pick_laps(range(67, 70))

telemetry_driver_1 = fastest_driver_1.get_telemetry().add_distance()
telemetry_driver_2 = fastest_driver_2.get_telemetry().add_distance()

# plotting.setup_mpl()

driver_1_style = plotting.driver_color(driver_1)
driver_2_style = plotting.driver_color(driver_2)


delta_time, ref_tel, compare_tel = utils.delta_time(fastest_driver_1, fastest_driver_2)


plot_size = [15, 15]
plot_title = f"{session.event.year} {session.event.EventName} - {session.name} - {driver_1} VS {driver_2}"
plot_ratios = [1, 3, 2, 1, 1, 2, 1]
plot_filename = plot_title.replace(" ", "") + ".png"

plt.rcParams['figure.figsize'] = plot_size

fig, ax = plt.subplots(7, gridspec_kw={'height_ratios': plot_ratios})

ax[0].title.set_text(plot_title)


ax[0].plot(ref_tel['Distance'], delta_time, driver_2_style)
ax[0].axhline(0, color=driver_1_style)
ax[0].set(ylabel=f"Gap to {driver_1} (s)")

labels = ["Speed", "Throttle", "Brake", "nGear", "RPM", "DRS"]

for i in range(6):
    ax[i+1].plot(telemetry_driver_1['Distance'], telemetry_driver_1[labels[i]], driver_1_style, label=driver_1)
    ax[i+1].plot(telemetry_driver_2['Distance'], telemetry_driver_2[labels[i]], driver_2_style, label=driver_2)
    ax[i+1].set(ylabel=labels[i])

    if labels[i] == "Speed":
        ax[i+1].legend(loc="lower right")
    elif labels[i] == "DRS":
        ax[i+1].set(xlabel='Lap distance (meters)')

# ax[1].plot(telemetry_driver_1['Distance'], telemetry_driver_1['Speed'], driver_1_style, label=driver_1)
# ax[1].plot(telemetry_driver_2['Distance'], telemetry_driver_2['Speed'], driver_2_style, label=driver_2)
# ax[1].set(ylabel='Speed')
# ax[1].legend(loc="lower right")

# ax[2].plot(telemetry_driver_1['Distance'], telemetry_driver_1['Throttle'], driver_1_style, label=driver_1)
# ax[2].plot(telemetry_driver_2['Distance'], telemetry_driver_2['Throttle'], driver_2_style, label=driver_2)
# ax[2].set(ylabel='Throttle')

# ax[3].plot(telemetry_driver_1['Distance'], telemetry_driver_1['Brake'], driver_1_style, label=driver_1)
# ax[3].plot(telemetry_driver_2['Distance'], telemetry_driver_2['Brake'], driver_2_style, label=driver_2)
# ax[3].set(ylabel='Brake')

# ax[4].plot(telemetry_driver_1['Distance'], telemetry_driver_1['nGear'], driver_1_style, label=driver_1)
# ax[4].plot(telemetry_driver_2['Distance'], telemetry_driver_2['nGear'], driver_2_style, label=driver_2)
# ax[4].set(ylabel='Gear')

# ax[5].plot(telemetry_driver_1['Distance'], telemetry_driver_1['RPM'], driver_1_style, label=driver_1)
# ax[5].plot(telemetry_driver_2['Distance'], telemetry_driver_2['RPM'], driver_2_style, label=driver_2)
# ax[5].set(ylabel='RPM')

# ax[6].plot(telemetry_driver_1['Distance'], telemetry_driver_1['DRS'], driver_1_style, label=driver_1)
# ax[6].plot(telemetry_driver_2['Distance'], telemetry_driver_2['DRS'], driver_2_style, label=driver_2)
# ax[6].set(ylabel='DRS')
# ax[6].set(xlabel='Lap distance (meters)')


for a in ax.flat:
    a.label_outer()
    
plt.savefig("./Formula1/testPics/"+plot_filename, dpi=600)
print(fastest_driver_1['LapTime'])
print(fastest_driver_2['LapTime'])
plt.show()