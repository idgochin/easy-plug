import io
import requests
from google.cloud import storage
from PIL import Image

# Google Cloud Storage settings
BUCKET_NAME = "easy-plug-qr"
IMAGE_NAME = "qrcode/EZP000101.png"
LOCAL_SAVE_PATH = "EZP000101.png"

# Authenticate using service account
client = storage.Client.from_service_account_json("easy-plug-store-94fa3306c1c6.json")

def download_image():
    """Download an image from Google Cloud Storage."""
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(IMAGE_NAME)
    
    # Download image as bytes
    image_bytes = blob.download_as_bytes()

    # Save the image locally
    with open(LOCAL_SAVE_PATH, "wb") as file:
        file.write(image_bytes)
    
    return LOCAL_SAVE_PATH

# Download and check the image
downloaded_image = download_image()

# Open and show the image
image = Image.open(downloaded_image)
image.show()
