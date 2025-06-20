# visualizer.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Ensure 'graphs' directory exists
os.makedirs("graphs", exist_ok=True)

def generate_dashboard(csv_path='final_output.csv'):
    if not os.path.exists(csv_path):
        print(f"❌ File not found: {csv_path}")
        return

    df = pd.read_csv(csv_path)

    # Convert DATE_TIME if available
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'])

    # === 1. Line Plot: AC Power & DC Power over Time ===
    if 'timestamp' in df.columns:
        plt.figure(figsize=(12, 6))
        plt.plot(df['timestamp'], df['ac_power'], label='AC Power (W)', color='blue')
        plt.plot(df['timestamp'], df['dc_power'], label='DC Power (W)', color='orange')
        plt.xlabel("Time")
        plt.ylabel("Power (W)")
        plt.title("AC & DC Power Over Time")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig("graphs/ac_dc_power_time.png")
        #plt.show()

    # === 2. Scatter Plot: Irradiation vs Power Output ===
    if 'irradiation' in df.columns:
        plt.figure(figsize=(10, 5))
        sns.scatterplot(x='irradiation', y='ac_power', data=df, color='green')
        plt.title("Irradiation vs AC Power Output")
        plt.xlabel("Irradiation (W/m²)")
        plt.ylabel("AC Power (W)")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig("graphs/irradiation_vs_ac.png")
        #plt.show()

    # === 3. Temperature Impact on Power ===
    if 'temperature' in df.columns:
        plt.figure(figsize=(10, 5))
        sns.scatterplot(x='temperature', y='ac_power', data=df, color='red')
        plt.title("Module Temperature vs AC Power Output")
        plt.xlabel("Module Temperature (°C)")
        plt.ylabel("AC Power (W)")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig("graphs/temp_vs_power.png")
        #plt.show()

    # Plot actual vs simulated AC power
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df["ac_power"], label="Actual AC Power", color='blue', linewidth=2)
    plt.plot(df.index, df["Sim_ac_power"], label="Simulated AC Power", color='orange', linestyle='--', linewidth=2)
    plt.title("Actual vs Simulated AC Power Over Time")
    plt.xlabel("Timestamp")
    plt.ylabel("AC Power (kW)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("graphs/Actual_vs_Simulated_AC_Power.png")


    # Plot actual vs simulated DC power
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df["dc_power"], label="Actual DC Power", color='blue', linewidth=2)
    plt.plot(df.index, df["Sim_dc_power"], label="Simulated DC Power", color='orange', linestyle='--', linewidth=2)
    plt.title("Actual vs Simulated DC Power Over Time")
    plt.xlabel("Timestamp")
    plt.ylabel("DC Power (kW)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("graphs/Actual_vs_Simulated_DC_Power.png")


    # === 6. Correlation Heatmap ===
    plt.figure(figsize=(8, 6))
    sns.heatmap(df.corr(numeric_only=True), annot=True, cmap='coolwarm', fmt=".2f")
    plt.title("Feature Correlation Heatmap")
    plt.tight_layout()
    plt.savefig("graphs/correlation_heatmap.png")
    #plt.show()


    print("✅ All visualizations saved in /graphs folder and shown successfully.")

generate_dashboard('merged_by_session.csv')