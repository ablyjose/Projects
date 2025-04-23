import fastf1 as ff1
from fastf1 import plotting

from matplotlib import pyplot as plt


ff1.Cache.enable_cache('Formula1/cache')

year, gp, session = 2025, "Bahrain", 'R'

race = ff1.get_session(year, gp, session)
race.load()

driver_1, driver_2 = 'LEC', 'HAM'

lap_driver_1 = race.laps.pick_drivers(driver_1).pick_laps(50)
lap_driver_2 = race.laps.pick_drivers(driver_2).pick_laps(50)

print(lap_driver_1[['Driver', 'LapTime', 'Stint', 'Compound', 'TyreLife']])
print(lap_driver_2[['Driver', 'LapTime', 'Stint', 'Compound', 'TyreLife']])

tele_1 = lap_driver_1.get_telemetry()
tele_2 = lap_driver_2.get_telemetry()

driver_1_style = plotting.get_driver_style(driver_1, ['color', 'linestyle'], ff1.get_session(2024, gp, session)) # get_driver_style not updated yet for 2025
driver_2_style = plotting.get_driver_style('SAI', ['color', 'linestyle'], ff1.get_session(2024, gp, session))


plot_size = [30, 30]
plot_title = f"{race.event.year} {race.event.EventName} - {race.name} - {driver_1} VS {driver_2}"
plot_ratios = [3, 2, 1, 2]
plot_filename = plot_title.replace(" ", "") + ".png"

plt.rcParams['figure.figsize'] = plot_size

fig, ax = plt.subplots(4, gridspec_kw={'height_ratios': plot_ratios})

ax[0].title.set_text(plot_title)


ax[0].plot(tele_1['Distance'], tele_1['Speed'], **driver_1_style, label=driver_1)
ax[0].plot(tele_2['Distance'], tele_2['Speed'], **driver_2_style, label=driver_2)
ax[0].set(ylabel='Speed')
ax[0].legend(loc="lower right")

ax[1].plot(tele_1['Distance'], tele_1['Throttle'], **driver_1_style, label=driver_1)
ax[1].plot(tele_2['Distance'], tele_2['Throttle'], **driver_2_style, label=driver_2)
ax[1].set(ylabel='Throttle')

ax[2].plot(tele_1['Distance'], tele_1['Brake'], **driver_1_style, label=driver_1)
ax[2].plot(tele_2['Distance'], tele_2['Brake'], **driver_2_style, label=driver_2)
ax[2].set(ylabel='Brake')

ax[3].plot(tele_1['Distance'], tele_1['RPM'], **driver_1_style, label=driver_1)
ax[3].plot(tele_2['Distance'], tele_2['RPM'], **driver_2_style, label=driver_2)
ax[3].set(ylabel='RPM')


plt.savefig("C:/Users/albys/PortProjects/Formula1/testPics/"+plot_filename, dpi=600)
plt.show()