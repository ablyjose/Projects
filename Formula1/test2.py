import fastf1 as ff1
from fastf1 import plotting
from fastf1 import utils
from fastf1.core import Laps

from matplotlib import pyplot as plt
from matplotlib.pyplot import figure

import numpy as np
import pandas as pd

ff1.Cache.enable_cache('C:/Users/albys/PortProjects/Formula1/cache')

year, gp, session = 2025, "Bahrain", 'R' 

quali = ff1.get_session(year, gp, session)
quali.load()

driver_1, driver_2 = 'LEC', 'HAM'

laps_driver_1 = quali.laps.pick_drivers(driver_1)
laps_driver_2 = quali.laps.pick_drivers(driver_2)

fastest_driver_1 = laps_driver_1.pick_fastest()
fastest_driver_2 = laps_driver_2.pick_fastest()

print(fastest_driver_1)
print()
print(fastest_driver_2)

telemetry_driver_1 = fastest_driver_1.get_telemetry().add_distance()
telemetry_driver_2 = fastest_driver_2.get_telemetry().add_distance()

driver_1_style = plotting.get_driver_style(driver_1, ['color', 'linestyle'], ff1.get_session(2024, "Japan", 'Q'))
driver_2_style = plotting.get_driver_style('SAI', ['color', 'linestyle'], ff1.get_session(2024, "Japan", 'Q'))


delta_time, ref_tel, compare_tel = utils.delta_time(fastest_driver_1, fastest_driver_2)


plot_size = [15, 15]
plot_title = f"{quali.event.year} {quali.event.EventName} - {quali.name} - {driver_1} VS {driver_2}"
plot_ratios = [1, 3, 2, 1, 1, 2, 1]
plot_filename = plot_title.replace(" ", "") + ".png"

plt.rcParams['figure.figsize'] = plot_size

fig, ax = plt.subplots(7, gridspec_kw={'height_ratios': plot_ratios})

ax[0].title.set_text(plot_title)


ax[0].plot(-ref_tel['Distance'], delta_time, **driver_1_style)
ax[0].axhline(0, **driver_2_style)
ax[0].set(ylabel=f"Gap to {driver_2} (s)")

ax[1].plot(telemetry_driver_1['Distance'], telemetry_driver_1['Speed'], **driver_1_style, label=driver_1)
ax[1].plot(telemetry_driver_2['Distance'], telemetry_driver_2['Speed'], **driver_2_style, label=driver_2)
ax[1].set(ylabel='Speed')
ax[1].legend(loc="lower right")

ax[2].plot(telemetry_driver_1['Distance'], telemetry_driver_1['Throttle'], **driver_1_style, label=driver_1)
ax[2].plot(telemetry_driver_2['Distance'], telemetry_driver_2['Throttle'], **driver_2_style, label=driver_2)
ax[2].set(ylabel='Throttle')

ax[3].plot(telemetry_driver_1['Distance'], telemetry_driver_1['Brake'], **driver_1_style, label=driver_1)
ax[3].plot(telemetry_driver_2['Distance'], telemetry_driver_2['Brake'], **driver_2_style, label=driver_2)
ax[3].set(ylabel='Brake')

ax[4].plot(telemetry_driver_1['Distance'], telemetry_driver_1['nGear'], **driver_1_style, label=driver_1)
ax[4].plot(telemetry_driver_2['Distance'], telemetry_driver_2['nGear'], **driver_2_style, label=driver_2)
ax[4].set(ylabel='Gear')

ax[5].plot(telemetry_driver_1['Distance'], telemetry_driver_1['RPM'], **driver_1_style, label=driver_1)
ax[5].plot(telemetry_driver_2['Distance'], telemetry_driver_2['RPM'], **driver_2_style, label=driver_2)
ax[5].set(ylabel='RPM')

ax[6].plot(telemetry_driver_1['Distance'], telemetry_driver_1['DRS'], **driver_1_style, label=driver_1)
ax[6].plot(telemetry_driver_2['Distance'], telemetry_driver_2['DRS'], **driver_2_style, label=driver_2)
ax[6].set(ylabel='DRS')
ax[6].set(xlabel='Lap distance (meters)')


for a in ax.flat:
    a.label_outer()
    
plt.savefig("./testPics/"+plot_filename, dpi=600)
plt.show()