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
    
    blob.delete()

    return True

# Delete the file
delete_success = delete_cs_file("easy-plug-qr", "qrcode/EZP000101.png")
print("Delete successful:", delete_success)
