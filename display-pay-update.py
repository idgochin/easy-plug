# import tkinter as tk
# from PIL import Image, ImageTk
# import requests
# from io import BytesIO
# import sys
# import time
# from google.cloud import storage
# import os
# import io

# # Set key credentials file path
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'easy-plug-store-94fa3306c1c6.json'

# # Initialize Google Cloud Storage Client
# client = storage.Client()

# # Read the parameter (e.g., EZP000101 or EZP000102)
# if len(sys.argv) != 2:
#     print("Usage: python3 display-pay.py <parameter>")
#     sys.exit(1)

# parameter = sys.argv[1]
# bucket_name = "easy-plug-qr"
# file_name = f"qrcode/{parameter}.png"
# new_file_name = f"qrcode/IMG{parameter[3:]}.png"
# image_url = f"https://storage.googleapis.com/{bucket_name}/{new_file_name}"

# # Function to check if the image exists in Google Cloud Storage
# def image_exists(bucket_name, file_name):
#     storage_client = storage.Client()
#     bucket = storage_client.bucket(bucket_name)
#     blob = bucket.blob(file_name)
#     return blob.exists()

# # Define function to rename a file in Cloud Storage
# def rename_cs_file(bucket_name, file_name, new_file_name):
#     storage_client = storage.Client()
#     bucket = storage_client.bucket(bucket_name)
    
#     # Get the blob (file) from bucket
#     blob = bucket.blob(file_name)

#     if blob.exists():  # Check if the file exists
#         # Copy blob to new file
#         new_blob = bucket.copy_blob(blob, bucket, new_file_name)
        
#         # Delete the old file
#         blob.delete()
        
#         return f"File renamed from '{file_name}' to '{new_file_name}' successfully."
#     else:
#         return f"File '{file_name}' not found."

# # Function to fetch image
# def fetch_image():
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
            
#             return  # Exit the loop if successful

#         except requests.exceptions.RequestException as e:
#             elapsed_time = time.time() - start_time
#             print(f"Error fetching the image: {e}")
#             if elapsed_time > timeout:
#                 print("Timeout reached. Exiting the script.")
#                 sys.exit(1)  # Exit if the timeout is exceeded
#             time.sleep(retry_interval)  # Wait before retrying

# def download_image_from_gcs(bucket_name, image_path):
#     """Download image from Google Cloud Storage into memory."""
#     bucket = client.bucket(bucket_name)
#     blob = bucket.blob(image_path)
#     return blob.download_as_bytes()

# def fetch_and_display_image():
#     """Fetch, resize, and display an image from Google Cloud Storage optimized for 3.5" display."""
#     timeout = 10  # Maximum wait time in seconds
#     retry_interval = 2  # Wait time between retries
#     start_time = time.time()

#     while True:
#         try:
#             image_bytes = download_image_from_gcs(bucket_name, new_file_name)

#             # Convert bytes to PIL Image
#             pil_image = Image.open(io.BytesIO(image_bytes))
            
#             # Rotate image -90 degrees (clockwise)
#             pil_image = pil_image.rotate(90, expand=True)  # 90 = -90 degrees clockwise

#             # Get screen dimensions
#             screen_width = root.winfo_screenwidth()
#             screen_height = root.winfo_screenheight()
            
#             # Calculate optimal size for 3.5" display with zoom
#             # Use 90% of the smaller dimension to ensure it fits well, then apply zoom
#             max_size = min(screen_width, screen_height) * 0.9
#             zoom_factor = 1.5  # Adjust this value: 1.0 = no zoom, 1.5 = 50% bigger, 2.0 = double size
#             max_size *= zoom_factor
            
#             # Get original image dimensions
#             original_width, original_height = pil_image.size
            
#             # Calculate scaling factor to fit within max_size while maintaining aspect ratio
#             scale_factor = min(max_size / original_width, max_size / original_height)
            
#             # Calculate new dimensions
#             new_width = int(original_width * scale_factor)
#             new_height = int(original_height * scale_factor)
            
#             print(f"Screen: {screen_width}x{screen_height}")
#             print(f"Original image: {original_width}x{original_height}")
#             print(f"Scaled image: {new_width}x{new_height}")
#             print(f"Scale factor: {scale_factor:.2f}")
#             print(f"Zoom factor: {zoom_factor}x")

#             # Resize the image with high quality resampling
#             pil_image = pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)

#             # Convert to a format suitable for Tkinter
#             tk_image = ImageTk.PhotoImage(pil_image)

#             # Clear any existing content
#             for widget in root.winfo_children():
#                 widget.destroy()

#             # Create a label in Tkinter to display the image
#             label = tk.Label(root, image=tk_image, bg="black")
#             label.image = tk_image  # Keep a reference to avoid garbage collection
#             label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
            
#             print("Fetch and display image successful")
#             return  # Exit the loop if successful

#         except Exception as e:
#             elapsed_time = time.time() - start_time
#             print(f"Error fetching the image: {e}")
#             if elapsed_time > timeout:
#                 print("Timeout reached. Exiting the script.")
#                 sys.exit(1)  # Exit if the timeout is exceeded
#             time.sleep(retry_interval)  # Wait before retrying

# # Create the main Tkinter window
# root = tk.Tk()
# root.title("QR Image Display - 3.5 inch")

# # Set fullscreen mode
# root.attributes('-fullscreen', True)
# root.configure(bg="black")
# root.config(cursor="none")
# # root.attributes('-topmost', True)

# # Exit fullscreen with the Escape key
# root.bind("<Escape>", lambda e: root.destroy())

# # Exit after 1 minutes
# root.after(60000, lambda: sys.exit())

# # Fetch and display the image (includes checking if it exists)
# fetch_image()
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
    """Fetch, resize, and display an image from Google Cloud Storage optimized for 3.5" display."""
    timeout = 10  # Maximum wait time in seconds
    retry_interval = 2  # Wait time between retries
    start_time = time.time()

    while True:
        try:
            image_bytes = download_image_from_gcs(bucket_name, new_file_name)

            # Convert bytes to PIL Image
            pil_image = Image.open(io.BytesIO(image_bytes))
            
            # Rotate image -90 degrees (clockwise)
            pil_image = pil_image.rotate(90, expand=True)  # 90 = -90 degrees clockwise

            # Get screen dimensions
            screen_width = root.winfo_screenwidth()
            screen_height = root.winfo_screenheight()
            
            # Calculate optimal size for 3.5" display with zoom
            # Use 90% of the smaller dimension to ensure it fits well, then apply zoom
            max_size = min(screen_width, screen_height) * 0.9
            zoom_factor = 1.5  # Adjust this value: 1.0 = no zoom, 1.5 = 50% bigger, 2.0 = double size
            max_size *= zoom_factor
            
            # Get original image dimensions
            original_width, original_height = pil_image.size
            
            # Calculate scaling factor to fit within max_size while maintaining aspect ratio
            scale_factor = min(max_size / original_width, max_size / original_height)
            
            # Calculate new dimensions
            new_width = int(original_width * scale_factor)
            new_height = int(original_height * scale_factor)
            
            print(f"Screen: {screen_width}x{screen_height}")
            print(f"Original image: {original_width}x{original_height}")
            print(f"Scaled image: {new_width}x{new_height}")
            print(f"Scale factor: {scale_factor:.2f}")
            print(f"Zoom factor: {zoom_factor}x")

            # Resize the image with high quality resampling
            pil_image = pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # Convert to a format suitable for Tkinter
            tk_image = ImageTk.PhotoImage(pil_image)

            # Clear any existing content
            for widget in root.winfo_children():
                widget.destroy()

            # Create a label in Tkinter to display the image
            label = tk.Label(root, image=tk_image, bg="black")
            label.image = tk_image  # Keep a reference to avoid garbage collection
            label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
            
            print("Fetch and display image successful")
            
            # Start 1-minute countdown AFTER successful image display
            root.after(60000, lambda: sys.exit())
            
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
root.title("QR Image Display - 3.5 inch")

# Set fullscreen mode
root.attributes('-fullscreen', True)
root.configure(bg="black")
root.config(cursor="none")
# root.attributes('-topmost', True)

# Exit fullscreen with the Escape key
root.bind("<Escape>", lambda e: root.destroy())

# Fetch and display the image (includes checking if it exists)
fetch_image()
fetch_and_display_image()

# Run the Tkinter event loop
root.mainloop()