import pandas as pd

import fastf1 as ff1
from fastf1.core import Laps

ff1.Cache.enable_cache('Formula1/cache')

session = 'Q'

year = int(input("Enter year: "))
gp = input("Enter Grand Prix name: ")

quali = ff1.get_session(year, gp, session)
quali.load(weather=False, messages=False, telemetry=False)


# Get the results dataframe which contains the best times for each session and driver status
try:
    results = quali.results
except Exception as e:
    print(f"Error accessing results: {e}")
    exit(1)

# Helper function to process a session (Q1, Q2, Q3)
def process_session(session_col, position_limit):
    # Filter drivers who participated in this session
    # We can approximate participation by position. 
    # Q1: Everyone (Position >= 1)
    # Q2: Top 15 from Q1 (usually), or anyone with a time in Q2? 
    # Using 'Position' alone might be tricky if penalties are applied, but generally correct for participation.
    # Better: Everyone has a Q1 time (or DNF in Q1). 
    # For Q2/Q3, checks are needed.

    # Actually, fastf1 Results df has Q1, Q2, Q3 columns. 
    # If a driver didn't participate in Q2, Q2 will be NaT.
    
    # We want to list all drivers who *qualified* for that session.
    # Standard rules: Q1 all; Q2 top 15 of Q1; Q3 top 10 of Q2.
    # But simpler: just look at who has a time or a specific status relative to that session?
    # No, because a crash in Q3 results in NaT but they participated.
    # So we use Position as a proxy.
    # Q1: positions 1-20 (or however many drivers)
    # Q2: positions 1-15
    # Q3: positions 1-10
    
    if position_limit == "ALL":
        session_drivers = results.copy()
    else:
        session_drivers = results[results['Position'] <= position_limit].copy()
    
    # Create a list to store processed data
    session_data = []
    
    dnf_time = pd.Timedelta(minutes=4)

    for i, row in session_drivers.iterrows():
        driver = row['Abbreviation']
        lap_time = row[session_col]
        status = row['Status']
        
        # Check for DNF / No Time
        if pd.isna(lap_time):
            # If they have no time, but are in this session list, they likely crashed or didn't set a time.
            # We assign a dummy time for sorting.
            display_time = "DNF"
            sort_time = dnf_time
            dnf_time += pd.Timedelta(minutes=1) # Increment so they stay in order of processing/grid if needed
        else:
            display_time = lap_time
            sort_time = lap_time
            
        session_data.append({
            'Driver': driver,
            'LapTime': display_time,
            'SortTime': sort_time
        })
        
    # Create DataFrame
    df = pd.DataFrame(session_data)
    
    # Sort
    df = df.sort_values(by='SortTime').reset_index(drop=True)
    
    # Calculate Delta (only for those with valid times)
    if not df.empty:
        pole_time = df.loc[0, 'SortTime']
        
        deltas = []
        for i, row in df.iterrows():
            if row['LapTime'] == "DNF":
                deltas.append("N/A")
            else:
                # 107% Rule check (usually only Q1 but user had it everywhere)
                # Valid pole time check
                if isinstance(pole_time, pd.Timedelta):
                     if row['SortTime'] > pole_time * 1.07:
                         # Mark as DNF? User logic was: if > 107%, set to DNF.
                         # But be careful, wet sessions etc. 
                         # User specifically asked for "detect drivers that were in the session but could not put up a lap time"
                         # The 107% logic was existing, I will preserve it but applied to valid times.
                         df.at[i, 'LapTime'] = "DNF"
                         deltas.append("N/A")
                     else:
                         delta = row['SortTime'] - pole_time
                         deltas.append(delta)
                else:
                     deltas.append("N/A")

        df['DeltaToPole'] = deltas
        
    df.index += 1
    return df

# Q1: positions 16-20 eliminated, but we show ALL.
q1_order = process_session('Q1', "ALL")
# Q2: positions 1-15 (usually)
q2_order = process_session('Q2', 15)
# Q3: positions 1-10
q3_order = process_session('Q3', 10)

print("Q1 Results")
print(q1_order[['Driver', 'LapTime', 'DeltaToPole']])
print("--------------------------------\n")

print("Q2 Results")
print(q2_order[['Driver', 'LapTime', 'DeltaToPole']])
print("--------------------------------\n")

print("Q3 Results")
print(q3_order[['Driver', 'LapTime', 'DeltaToPole']])
print("--------------------------------\n")
