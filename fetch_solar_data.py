import requests
import pandas as pd
import os
from datetime import datetime
import pvlib
import time
# Location
LAT, LON = 18.4663, 73.8544  # Pune
TZ = 'Asia/Kolkata'

# File paths
file_path = r"C:\Users\shrot\PycharmProjects\Solar_DT\solar_data.csv"
sim_csv = r"C:\Users\shrot\PycharmProjects\Solar_DT\sim_input.csv"

# PV system configuration
modules_per_string = 5
parallel_strings = 66
total_modules = modules_per_string * parallel_strings
module_power = 305.226  # W
module_efficiency = 0.181
module_area = 1.63  # m²
area = total_modules * module_area

# === Determine next session ID (int) ===
def get_next_session_id(csv_path):
    if os.path.exists(csv_path):
        try:
            df = pd.read_csv(csv_path)
            if 'session_id' in df.columns and not df.empty:
                return int(df['session_id'].max()) + 1
        except:
            pass
    return 1  # Start from 1 if file doesn't exist or is unreadable

# === Main function ===
def fetch_and_simulate():
    session_id = get_next_session_id(file_path)

    url = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&current=temperature_2m,shortwave_radiation"
    time.sleep(5)
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if "current" in data:
            temperature = data["current"]["temperature_2m"]
            irradiation = data["current"]["shortwave_radiation"]
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Simulate using PVLib
            location = pvlib.location.Location(LAT, LON, tz=TZ)
            solpos = location.get_solarposition(pd.DatetimeIndex([current_time]))

            poa_irrad = pvlib.irradiance.get_total_irradiance(
                surface_tilt=20,
                surface_azimuth=180,
                solar_zenith=solpos['zenith'],
                solar_azimuth=solpos['azimuth'],
                dni=0, ghi=irradiation, dhi=0
            )

            effective_irradiance = poa_irrad['poa_global'].values[0]
            dc_power = module_efficiency * area * effective_irradiance / 10  # kW
            ac_power = 0.96 * dc_power

            print(f"[Session {session_id}] {current_time} | Temp: {temperature}°C | Irrad: {irradiation} W/m² | DC: {dc_power:.2f} kW | AC: {ac_power:.2f} kW")

            # Save to solar_data.csv
            df = pd.DataFrame([{
                "timestamp": current_time,
                "session_id": session_id,
                "temperature": temperature,
                "irradiation": irradiation,
                "dc_power": round(dc_power, 2),
                "ac_power": round(ac_power, 2)
            }])
            file_exists = os.path.isfile(file_path)
            df.to_csv(file_path, mode='a', header=not file_exists, index=False)

            # Save to sim_input.csv
            df[["session_id", "temperature", "irradiation"]].to_csv(sim_csv, index=False)

        else:
            print("API response missing 'current' key.")
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")

# === Run ===
fetch_and_simulate()
