import subprocess
import os
import sys
import pandas as pd

# === Paths ===
project_root = os.getcwd()

fetch_script = os.path.join(project_root, 'fetch_solar_data.py')
etl_script = os.path.join(project_root, 'ETL.py')
simulink_model = 'PVArrayGrid.slx'
matlab_export_script = 'sim_to_csv'

# === STEP 1: Fetch real data and simulate PV output using PVLib ===
print("\n🚀 Step 1: Fetching solar data & simulating via PVLib...")
subprocess.run([sys.executable, fetch_script], check=True)

# === STEP 2: Run Simulink model and export data ===
print("\n🔧 Step 2: Running MATLAB Simulink model & exporting data...")
matlab_cmd = f"cd('{project_root}'); load_system('{simulink_model}'); sim('{simulink_model}'); {matlab_export_script}; exit;"
subprocess.run(["matlab", "-batch", matlab_cmd], check=True)

# === STEP 3: Run ETL script to merge and clean data ===
print("\n🔗 Step 3: Merging real and simulated data via ETL.py...")
subprocess.run([sys.executable, etl_script], check=True)

print("\n✅ DONE! Your merged data pipeline ran successfully.")

print("\n🤖 Running ML Models...")


from arima import train_sarima
train_sarima(pd.read_csv("merged_by_session.csv"), column='AC_POWER')


from Fault_Detection import detect_faults
df = pd.read_csv("merged_by_session.csv")
faults = detect_faults(df)
faults.to_csv("faults_detected.csv", index=False)

from visualizer import generate_dashboard
generate_dashboard('merged_by_session.csv')
