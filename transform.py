import duckdb
import os
import polars as pl
from azure.storage.blob import BlobServiceClient

# --- !! AZURE CONFIGURATION !! ---
CONNECT_STR = os.environ.get('AZURE_STORAGE_CONNECTION_STRING') 
RAW_CONTAINER = 'raw-data'
RAW_BLOB = 'raw/carts.json'
azure_raw_path = f'az://{RAW_CONTAINER}/{RAW_BLOB}'

# --- NEW: Configuration for our processed data ---
PROCESSED_CONTAINER = 'processed-data'
PROCESSED_BLOB_NAME = 'kpis/daily_sales_summary.csv' # We'll save as CSV
LOCAL_TEMP_FILE = 'daily_sales_summary.csv'        # A temporary local file

# This is *only* the final SELECT query
# We moved the other commands into the function
transform_sql_query = f"""
SELECT
    SUM(p.quantity) AS total_items_sold,
    COUNT(DISTINCT carts.id) AS total_carts,
    MIN(carts.date) AS first_sale_date,
    MAX(carts.date) AS last_sale_date
FROM 
    read_json_auto('{azure_raw_path}') AS carts, -- Reads the JSON from Azure
    UNNEST(carts.products) AS t(p); -- Expands the nested 'products' array
"""

def upload_file_to_azure(local_file, container_name, blob_name):
    """Uploads a single file to Azure Blob Storage."""
    print(f"\nAttempting to upload '{local_file}' to Azure container '{container_name}'...")
    try:
        blob_service_client = BlobServiceClient.from_connection_string(CONNECT_STR)
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        
        with open(local_file, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)
            
        print(f"Successfully uploaded '{blob_name}' to '{container_name}'.")
        return True
    except Exception as e:
        print(f"Error uploading file: {e}")
        return False

def transform_cloud_data():
    if not CONNECT_STR:
        print("Error: AZURE_STORAGE_CONNECTION_STRING environment variable not set.")
        return

    print("Starting data transformation with DuckDB (reading from Azure)...")
    try:
        # Connect to an in-memory database
        con = duckdb.connect(database=':memory:')
        
        # --- FIX: Run each command separately ---
        print("1. Installing Azure extension...")
        con.execute("INSTALL azure;")
        
        print("2. Loading Azure extension...")
        con.execute("LOAD azure;")
        
        print("3. Setting Azure connection string...")
        # Here we pass the parameter *only* to the SET command
        con.execute("SET azure_storage_connection_string = ?;", [CONNECT_STR])
        
        print("4. Running transformation query...")
        # Now we run the main query, which has no parameters
        result_df = con.execute(transform_sql_query).pl()
        # --- END FIX ---
        
        print("\n--- Transformed Data (Results) ---")
        print(result_df)
        
        print(f"\n5. Saving transformed data to local file: '{LOCAL_TEMP_FILE}'")
        result_df.write_csv(LOCAL_TEMP_FILE)
        
        print("\n6. Uploading transformed data to Azure...")
        upload_file_to_azure(LOCAL_TEMP_FILE, PROCESSED_CONTAINER, PROCESSED_BLOB_NAME)

        print("\n--- ELT Process Complete! ---")

    except Exception as e:
        print(f"Error during transformation: {e}")

# --- Run the script ---
if __name__ == "__main__":
    transform_cloud_data()