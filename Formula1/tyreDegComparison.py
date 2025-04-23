import fastf1 as ff1
from fastf1 import plotting

from matplotlib import pyplot as plt


ff1.Cache.enable_cache('Formula1/cache')

# year, gp, session = 2025, "Bahrain", 'FP2'
# fp = ff1.get_session(year, gp, session)
# fp.load()

testing = ff1.get_testing_session(2024, 1, 1)
print(testing.api_path)
testing.load()

print(testing.laps)