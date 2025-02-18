# import tkinter as tk
# from PIL import Image, ImageTk
# import requests
# from io import BytesIO
# import sys
# import time

# # Read the parameter (e.g., EZP000101 or EZP000102)
# if len(sys.argv) != 2:
#     print("Usage: python3 display-pay.py <parameter>")
#     sys.exit(1)

# parameter = sys.argv[1]
# image_url = f"https://storage.googleapis.com/easy-plug-qr/qrcode/{parameter}.png"

# # Function to fetch and display the image
# def fetch_and_display_image():
#     start_time = time.time()  # Record the start time
#     retry_interval = 5  # Retry every 5 seconds
#     timeout = 5 * 60  # Maximum wait time: 5 minutes

#     while True:
#         try:
#             # Fetch the image from the URL
#             response = requests.get(image_url)
#             response.raise_for_status()  # Raise an error for bad status codes
#             image_data = BytesIO(response.content)

#             # Open the image using Pillow
#             pil_image = Image.open(image_data)

#             # Calculate new dimensions (230% of original)
#             original_width, original_height = pil_image.size
#             new_width = int(original_width * 2.3)
#             new_height = int(original_height * 2.3)

#             # Resize the image
#             pil_image = pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)

#             # Convert to a format suitable for Tkinter
#             tk_image = ImageTk.PhotoImage(pil_image)

#             # Create a label in Tkinter to display the image
#             label = tk.Label(root, image=tk_image, bg="black")
#             label.image = tk_image  # Keep a reference to avoid garbage collection
#             label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
#             return  # Exit the loop if successful

#         except requests.exceptions.RequestException as e:
#             elapsed_time = time.time() - start_time
#             print(f"Error fetching the image: {e}")
#             if elapsed_time > timeout:
#                 print("Timeout reached. Exiting the script.")
#                 sys.exit(1)  # Exit if the timeout is exceeded
#             time.sleep(retry_interval)  # Wait before retrying

# # Create the main Tkinter window
# root = tk.Tk()
# root.title("Zoomed Image Display")

# # Set fullscreen mode
# root.attributes('-fullscreen', True)
# root.configure(bg="black")

# # Exit fullscreen with the Escape key
# root.bind("<Escape>", lambda e: root.destroy())

# # Fetch and display the image
# fetch_and_display_image()

# # Run the Tkinter event loop
# root.mainloop()

import tkinter as tk
from PIL import Image, ImageTk
import requests
from io import BytesIO
import sys
import time
from google.cloud import storage
import os
import io

# Set key credentials file path
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'easy-plug-store-94fa3306c1c6.json'

# Initialize Google Cloud Storage Client
client = storage.Client()

# Read the parameter (e.g., EZP000101 or EZP000102)
if len(sys.argv) != 2:
    print("Usage: python3 display-pay.py <parameter>")
    sys.exit(1)

parameter = sys.argv[1]
bucket_name = "easy-plug-qr"
file_name = f"qrcode/{parameter}.png"
new_file_name = f"qrcode/IMG{parameter[3:]}.png"
image_url = f"https://storage.googleapis.com/{bucket_name}/{new_file_name}"

# Function to check if the image exists in Google Cloud Storage
def image_exists(bucket_name, file_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    return blob.exists()

# Define function to rename a file in Cloud Storage
def rename_cs_file(bucket_name, file_name, new_file_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    
    # Get the blob (file) from bucket
    blob = bucket.blob(file_name)

    if blob.exists():  # Check if the file exists
        # Copy blob to new file
        new_blob = bucket.copy_blob(blob, bucket, new_file_name)
        
        # Delete the old file
        blob.delete()
        
        return f"File renamed from '{file_name}' to '{new_file_name}' successfully."
    else:
        return f"File '{file_name}' not found."

# Function to fetch and display the image
# def fetch_and_display_image():
#     start_time = time.time()  # Record the start time
#     retry_interval = 5  # Retry every 5 seconds
#     timeout = 5 * 60  # Maximum wait time: 5 minutes

#     while True:
#         if not image_exists(bucket_name, file_name):
#             elapsed_time = time.time() - start_time
#             print(f"Image '{file_name}' does not exist in the bucket.")
#             if elapsed_time > timeout:
#                 print("Timeout reached. Exiting the script.")
#                 sys.exit(1)  # Exit if the timeout is exceeded
#             time.sleep(retry_interval)  # Wait before retrying
#             continue  # Retry the check

#         try:
#             # Rename the file
#             rename_result = rename_cs_file(bucket_name, file_name, new_file_name)
#             print(rename_result)
#             # Fetch the image from the URL
#             response = requests.get(image_url)
#             response.raise_for_status()  # Raise an error for bad status codes
#             image_data = BytesIO(response.content)

#             # Open the image using Pillow
#             pil_image = Image.open(image_data)

#             # Calculate new dimensions (230% of original)
#             original_width, original_height = pil_image.size
#             new_width = int(original_width * 2.3)
#             new_height = int(original_height * 2.3)

#             # Resize the image
#             pil_image = pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)

#             # Convert to a format suitable for Tkinter
#             tk_image = ImageTk.PhotoImage(pil_image)

#             # Create a label in Tkinter to display the image
#             label = tk.Label(root, image=tk_image, bg="black")
#             label.image = tk_image  # Keep a reference to avoid garbage collection
#             label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
#             return  # Exit the loop if successful

#         except requests.exceptions.RequestException as e:
#             elapsed_time = time.time() - start_time
#             print(f"Error fetching the image: {e}")
#             if elapsed_time > timeout:
#                 print("Timeout reached. Exiting the script.")
#                 sys.exit(1)  # Exit if the timeout is exceeded
#             time.sleep(retry_interval)  # Wait before retrying

# Function to fetch image
def fetch_image():
    start_time = time.time()  # Record the start time
    retry_interval = 5  # Retry every 5 seconds
    timeout = 5 * 60  # Maximum wait time: 5 minutes

    while True:
        if not image_exists(bucket_name, file_name):
            elapsed_time = time.time() - start_time
            print(f"Image '{file_name}' does not exist in the bucket.")
            if elapsed_time > timeout:
                print("Timeout reached. Exiting the script.")
                sys.exit(1)  # Exit if the timeout is exceeded
            time.sleep(retry_interval)  # Wait before retrying
            continue  # Retry the check

        try:
            # Rename the file
            rename_result = rename_cs_file(bucket_name, file_name, new_file_name)
            print(rename_result)
            
            return  # Exit the loop if successful

        except requests.exceptions.RequestException as e:
            elapsed_time = time.time() - start_time
            print(f"Error fetching the image: {e}")
            if elapsed_time > timeout:
                print("Timeout reached. Exiting the script.")
                sys.exit(1)  # Exit if the timeout is exceeded
            time.sleep(retry_interval)  # Wait before retrying

def download_image_from_gcs(bucket_name, image_path):
    """Download image from Google Cloud Storage into memory."""
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(image_path)
    return blob.download_as_bytes()

def fetch_and_display_image():
    """Fetch, resize, and display an image from Google Cloud Storage."""
    timeout = 10  # Maximum wait time in seconds
    retry_interval = 2  # Wait time between retries
    start_time = time.time()

    while True:
        try:
            image_bytes = download_image_from_gcs(bucket_name, new_file_name)

            # Convert bytes to PIL Image
            pil_image = Image.open(io.BytesIO(image_bytes))

            # Calculate new dimensions (230% of original)
            original_width, original_height = pil_image.size
            new_width = int(original_width * 2.3)
            new_height = int(original_height * 2.3)

            # Resize the image
            pil_image = pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # Convert to a format suitable for Tkinter
            tk_image = ImageTk.PhotoImage(pil_image)

            # Create a label in Tkinter to display the image
            label = tk.Label(root, image=tk_image, bg="black")
            label.image = tk_image  # Keep a reference to avoid garbage collection
            label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
            print("fetch and display image successful")
            return  # Exit the loop if successful

        except Exception as e:
            elapsed_time = time.time() - start_time
            print(f"Error fetching the image: {e}")
            if elapsed_time > timeout:
                print("Timeout reached. Exiting the script.")
                sys.exit(1)  # Exit if the timeout is exceeded
            time.sleep(retry_interval)  # Wait before retrying

# Create the main Tkinter window
root = tk.Tk()
root.title("Zoomed Image Display")

# Set fullscreen mode
root.attributes('-fullscreen', True)
root.configure(bg="black")

# Exit fullscreen with the Escape key
root.bind("<Escape>", lambda e: root.destroy())

# Fetch and display the image (includes checking if it exists)
fetch_image()
fetch_and_display_image()

# Run the Tkinter event loop
root.mainloop()

