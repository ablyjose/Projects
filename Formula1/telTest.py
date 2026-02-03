import fastf1 as ff1
import os
from fastf1 import plotting
from fastf1 import utils
from fastf1.core import Laps

from matplotlib import pyplot as plt
from matplotlib.pyplot import figure

import numpy as np
import pandas as pd

ff1.Cache.enable_cache('Formula1/cache')

year, gp, session_name = int(input("Year: ")), input("GP: "), input("Session: ")

session = ff1.get_event(year, gp).get_session(session_name)
session.load(weather=False)

driver_1, driver_2 = input("Driver 1: "), input("Driver 2: ")

match session_name:
    case 'FP1' | 'FP2' | 'FP3':
        driver_1_laps = session.laps.pick_drivers(driver_1)
        driver_2_laps = session.laps.pick_drivers(driver_2)

        fastest_driver_1 = driver_1_laps.pick_fastest()
        fastest_driver_2 = driver_2_laps.pick_fastest()
    case 'Q':
        q1_driver_1, q2_driver_1, q3_driver_1 = session.laps.pick_drivers(driver_1).split_qualifying_sessions()
        q1_driver_2, q2_driver_2, q3_driver_2 = session.laps.pick_drivers(driver_2).split_qualifying_sessions()

        fastest_driver_1 = q3_driver_1.pick_fastest()
        fastest_driver_2 = q3_driver_2.pick_fastest()
    case 'R':
        driver_1_laps = session.laps.pick_drivers(driver_1)
        driver_2_laps = session.laps.pick_drivers(driver_2)

        lap_1 = input("Lap for " + driver_1 + " ('fastest' or number): ")
        lap_2 = input("Lap for " + driver_2 + " ('fastest' or number): ")

        if lap_1 == "fastest":
            fastest_driver_1 = driver_1_laps.pick_fastest()
        else:
            fastest_driver_1 = driver_1_laps.pick_laps(int(lap_1))
        
        if lap_2 == "fastest":
            fastest_driver_2 = driver_2_laps.pick_fastest()
        else:
            fastest_driver_2 = driver_2_laps.pick_laps(int(lap_2))
    case _:
        print("Session not recognized")

telemetry_driver_1 = fastest_driver_1.get_telemetry().add_distance()
telemetry_driver_2 = fastest_driver_2.get_telemetry().add_distance()

# plotting.setup_mpl()


driver_colors = {
    'NOR': '#D2FF00',
    'PIA': '#FF8F00',
    'RUS': '#00D2BE',
    'ANT': '#ADD8E6',
    'VER': '#1E2A78',
    'TSU': '#1A2C80',
    'LEC': '#DC0000',
    'HAM': '#800080',
    'ALB': '#FFCCC7',
    'SAI': '#0082FA',
    'HAD': '#12264F',
    'LAW': '#F9F871',
    'ALO': '#006F62',
    'STR': '#006F62',
    'OCO': '#F7F7F7',
    'BEA': '#FF007F',
    'HUL': '#39FF14',
    'BOR': '#009739',
    'GAS': '#4E90FF',
    'COL': '#04299C',
}

driver_1_color = driver_colors[driver_1]
driver_2_color = driver_colors[driver_2]

driver2s = {'NOR', 'ANT', 'TSU', 'HAM', 'SAI', 'LAW', 'ALO', 'BEA', 'BOR', 'COL'}

driver_1_style = {'color': driver_1_color, 'linestyle': '-'}
driver_2_style = {'color': driver_2_color, 'linestyle': '-'}

if (driver_1 in driver2s):
    driver_1_style['linestyle'] = '--'
elif (driver_2 in driver2s):
    driver_2_style['linestyle'] = '--'

delta_time, ref_tel, compare_tel = utils.delta_time(fastest_driver_1, fastest_driver_2)

plot_size = [15, 15]
plot_title = f"{session.event.year} {session.event.EventName} - {session.name} - {driver_1} VS {driver_2}"
plot_ratios = [1, 3, 2, 1, 1, 2, 1]
plot_filename = plot_title.replace(" ", "") + ".png"

plt.rcParams['figure.figsize'] = plot_size
bg_color = '#2b2b2b'
fg_color = '#FFFFFF'
fig, ax = plt.subplots(7, gridspec_kw={'height_ratios': plot_ratios}, facecolor=bg_color)

ax[0].title.set_text(plot_title)
ax[0].title.set_color(fg_color)

ax[0].plot(ref_tel['Distance'], delta_time, **driver_2_style)
ax[0].axhline(0, color=driver_1_style['color'])
ax[0].set(ylabel=f"Gap to {driver_1} (s)")

for a in ax.flat:
    a.set_facecolor(bg_color)
    # spine and tick colors
    for spine in a.spines.values():
        spine.set_color(fg_color)
    a.tick_params(colors=fg_color)
    # label color
    a.yaxis.label.set_color(fg_color)
    a.xaxis.label.set_color(fg_color)
    # grid (optional subtle grid)
    a.grid(True, color=fg_color, alpha=0.08)
    # legend text/frame colors
    lg = a.get_legend()
    if lg is not None:
        for text in lg.get_texts():
            text.set_color(fg_color)
        frame = lg.get_frame()
        frame.set_facecolor(bg_color)
        frame.set_edgecolor(fg_color)
        frame.set_alpha(0.2)

labels = ["Speed", "Throttle", "Brake", "nGear", "RPM", "DRS"]

for i in range(6):
    ax[i+1].plot(telemetry_driver_1['Distance'], telemetry_driver_1[labels[i]], **driver_1_style, label=driver_1)
    ax[i+1].plot(telemetry_driver_2['Distance'], telemetry_driver_2[labels[i]], **driver_2_style, label=driver_2)
    ax[i+1].set(ylabel=labels[i])

    if labels[i] == "Speed":
        ax[i+1].legend(loc="lower right")
    elif labels[i] == "DRS":
        ax[i+1].set(xlabel='Lap distance (meters)')

for a in ax.flat:
    a.label_outer()
    
if not os.path.exists("./Formula1/testPics"):
    os.makedirs("./Formula1/testPics")

plt.savefig("./Formula1/testPics/"+plot_filename, dpi=600, facecolor=bg_color)
print(fastest_driver_1['LapTime'])
print(fastest_driver_2['LapTime'])
plt.show()