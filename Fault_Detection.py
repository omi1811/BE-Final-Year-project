import pandas as pd

def detect_faults(df, threshold=0.15):
    df['PREDICTED_AC'] = df['Sim_ac_power']
    df['ACTUAL_AC'] = df['ac_power']

    df['ABS_ERROR'] = abs(df['Sim_ac_power'] - df['ac_power'])
    df['REL_ERROR'] = df['Sim_ac_power'] / (df['ac_power'] + 1e-5)
    df['FAULT'] = df['REL_ERROR'] > threshold

    fault_rows = df[df['FAULT']]
    for col in ['PREDICTED_AC', 'ACTUAL_AC', 'ABS_ERROR', 'REL_ERROR', 'FAULT']:
        if col in df.columns:
            df.drop(columns=[col], inplace=True)
    print(f"⚠️ Detected {len(fault_rows)} fault(s).")
    return fault_rows
