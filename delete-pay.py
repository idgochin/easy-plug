# # import packages
# from google.cloud import storage
# import os
# import sys

# # set key credentials file path
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'easy-plug-store-94fa3306c1c6.json'

# # define function that deletes a file from the bucket
# def delete_cs_file(bucket_name, file_name):
#     storage_client = storage.Client()
#     bucket = storage_client.bucket(bucket_name)
#     blob = bucket.blob(file_name)
    
#     blob.delete()
#     return True

# # Get plug ID from command-line arguments
# if len(sys.argv) < 2:
#     print("Error: No plug ID provided.")
#     sys.exit(1)

# plug_id = sys.argv[1]

# # Define the file to delete
# file_name = f"qrcode/{plug_id}.png"

# # Delete the file
# delete_success = delete_cs_file("easy-plug-qr", file_name)
# print(f"Delete successful for {file_name}:", delete_success)

# Import packages
from google.cloud import storage
import os
import sys

# Set key credentials file path
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'easy-plug-store-94fa3306c1c6.json'

# Define function that deletes a file from the bucket if it exists
def delete_cs_file(bucket_name, file_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    
    if blob.exists():
        blob.delete()
        print(f"File '{file_name}' deleted successfully.")
        return True
    else:
        print(f"File '{file_name}' does not exist.")
        return False

# Get plug ID from command-line arguments
if len(sys.argv) < 2:
    print("Error: No plug ID provided.")
    sys.exit(1)

plug_id = sys.argv[1]

# Define the file to delete
file_name = f"qrcode/IMG{plug_id[3:]}.png"

# Attempt to delete the file
delete_success = delete_cs_file("easy-plug-qr", file_name)
print(f"Delete operation result for {file_name}: {delete_success}")

