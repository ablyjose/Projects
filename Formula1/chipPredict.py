import fastf1 as ff1
from fastf1.ergast import Ergast

ff1.Cache.enable_cache('Formula1/cache')

def get_drivers_standings():
    ergast = Ergast()
    standings = ergast.get_driver_standings(season=2024)
    return standings

print(get_drivers_standings())