# import packages
from google.cloud import storage
import os

# set key credentials file path
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'easy-plug-store-94fa3306c1c6.json'

# define function that deletes a file from the bucket
def delete_cs_file(bucket_name, file_name):
    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    print(blob.exists())
    
    blob.delete()

    return True

# Delete the file
delete_success = delete_cs_file("easy-plug-qr", "qrcode/IMG000101.png")
print("Delete successful:", delete_success)

# from google.cloud import storage
# import os

# # Set key credentials file path
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "easy-plug-store-94fa3306c1c6.json"

# def permanently_delete_all_versions(bucket_name, file_name):
#     storage_client = storage.Client()
#     bucket = storage_client.bucket(bucket_name)

#     # List all versions of the file
#     blobs = list(bucket.list_blobs(prefix=file_name, versions=True))

#     if not blobs:
#         print(f"No versions found for: {file_name}")
#         return False

#     # Delete all versions
#     for blob in blobs:
#         print(f"Deleting version {blob.generation} of {blob.name}")
#         blob.delete()

#     print(f"All versions of '{file_name}' have been permanently deleted.")
#     return True

# # Call the function to delete all versions of the file
# delete_success = permanently_delete_all_versions("easy-plug-qr", "qrcode/EZP000101.png")
# print("Delete successful:", delete_success)
