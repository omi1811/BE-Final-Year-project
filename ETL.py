import pandas as pd
from azure.storage.blob import BlobServiceClient
   from dotenv import load_dotenv
   import os

   load_dotenv()



# === File paths ===
real_data_path = os.getenv("real_data_path")
simulated_data_path = os.getenv("simulated_data_path")
output_path = os.getenv("output_path")

# === Load both CSVs ===
real_df = pd.read_csv(real_data_path)
real_df = real_df.drop_duplicates()
sim_df = pd.read_csv(simulated_data_path)
sim_df = sim_df.drop_duplicates()

# === Rename columns in sim_df for clarity ===
sim_df = sim_df.rename(columns={
    'AC_Power': 'Sim_ac_power',
    'DC_Power': 'Sim_dc_power'
})

# === Merge on session_id ===
merged_df = pd.merge(
    real_df,
    sim_df[['session_id', 'Sim_dc_power', 'Sim_ac_power']],
    on='session_id',
    how='inner'
)

final_df = merged_df[[
    'session_id',
    'timestamp',
    'temperature',
    'irradiation',
    'dc_power',
    'ac_power',
    'Sim_dc_power',
    'Sim_ac_power'
]]


final_df['Sim_ac_power'] = final_df['Sim_ac_power'].apply(lambda x: max(x, 0))
final_df['Sim_dc_power'] = final_df['Sim_dc_power'].apply(lambda x: max(x, 0))

# === Export ===
final_df.to_csv(output_path, index=False)
print(f"✅ Merged file saved at: {output_path}")

def upload_to_azure(file_path, container_name, blob_name):
    try:
        connect_str = os.getenv("Conn_string")
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

        with open(file_path, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)

        print(f"🚀 Uploaded {file_path} to Azure Blob Storage as '{blob_name}'")
    except Exception as e:
        print(f"❌ Upload failed: {e}")

# Call the upload function
upload_to_azure(output_path, "solar-data", "Final_Merged_CSV")
