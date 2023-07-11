import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Read the values from environment variables
azure_delta_lake_path = os.getenv('azure_delta_lake_path')
local_delta_lake_path = os.getenv('local_delta_lake_path')
azure_storage_account_name = os.getenv('azure_storage_account_name')
azure_storage_account_key = os.getenv('azure_storage_account_key')

