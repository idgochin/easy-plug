# Import packages
from google.cloud import storage
import os

# Set key credentials file path
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'easy-plug-store-94fa3306c1c6.json'

# Define function to rename a file in Cloud Storage
def rename_cs_file(bucket_name, old_file_name, new_file_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    
    # Get the blob (file) from bucket
    blob = bucket.blob(old_file_name)

    if blob.exists():  # Check if the file exists
        # Copy blob to new file
        new_blob = bucket.copy_blob(blob, bucket, new_file_name)
        
        # Delete the old file
        blob.delete()
        
        return f"File renamed from '{old_file_name}' to '{new_file_name}' successfully."
    else:
        return f"File '{old_file_name}' not found."

# Rename the file
rename_result = rename_cs_file("easy-plug-qr", "qrcode/EZP000101.png", "qrcode/IMG000101.png")
print(rename_result)
