import requests
import json
import os
from azure.storage.blob import BlobServiceClient # <-- NEW: Import Azure library

# --- CONFIGURATION ---
API_URL = "https://fakestoreapi.com/carts"
LOCAL_FILE = 'carts.json'

# --- !! AZURE CONFIGURATION !! ---
# The script will get this from the environment variable you just set
CONNECT_STR = os.environ.get('AZURE_STORAGE_CONNECTION_STRING') 
AZURE_CONTAINER_NAME = 'raw-data'  # <-- This is the container name you created
AZURE_BLOB_NAME = 'raw/carts.json'       # This is the file path *inside* the container

def fetch_cart_data():
    """Fetches sales cart data from the FakeStoreAPI."""
    print(f"Attempting to fetch data from {API_URL}...")
    try:
        response = requests.get(API_URL)
        response.raise_for_status() 
        data = response.json()
        print(f"Successfully fetched {len(data)} cart records.")
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error: Failed to fetch data from API. {e}")
        return None

def save_data_locally(data, file_path):
    """Saves the data to a local file."""
    try:
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Successfully saved raw data locally to: {file_path}")
        return True
    except IOError as e:
        print(f"Error: Could not write to local file. {e}")
        return False

def upload_to_azure_blob(local_file_path, container_name, blob_name):
    """Uploads a local file to Azure Blob Storage."""
    if not CONNECT_STR:
        print("Error: AZURE_STORAGE_CONNECTION_STRING environment variable not set.")
        print("Please set this variable in your terminal before running.")
        return False
        
    print(f"\nAttempting to upload {local_file_path} to Azure container '{container_name}' as '{blob_name}'...")
    try:
        # Create the BlobServiceClient using the connection string
        blob_service_client = BlobServiceClient.from_connection_string(CONNECT_STR)
        
        # Get a client for the specific blob
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        
        # Upload the local file
        with open(local_file_path, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)
            
        print("Successfully uploaded to Azure Blob Storage.")
        return True
        
    except Exception as e:
        print(f"Error uploading to Azure: {e}")
        return False

# --- Run the script ---
if __name__ == "__main__":
    cart_data = fetch_cart_data()
    
    if cart_data:
        # 'L' Step 1: Save locally first
        if save_data_locally(cart_data, LOCAL_FILE):
            
            # 'L' Step 2: Upload to Azure Blob (our Data Lake)
            upload_to_azure_blob(LOCAL_FILE, AZURE_CONTAINER_NAME, AZURE_BLOB_NAME)pip