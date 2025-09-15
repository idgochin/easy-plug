import os
import io
import time
import sys
import tkinter as tk
from google.cloud import storage
from PIL import Image, ImageTk

# Set Google Cloud credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "easy-plug-store-94fa3306c1c6.json"

# Initialize Google Cloud Storage Client
client = storage.Client()

# Define bucket and image path
BUCKET_NAME = "easy-plug-qr"
IMAGE_PATH = "qrcode/EZP000101.png"

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
            image_bytes = download_image_from_gcs(BUCKET_NAME, IMAGE_PATH)

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
root.attributes('-topmost', True)

# Exit fullscreen with the Escape key
root.bind("<Escape>", lambda e: root.destroy())

# Fetch and display the image
fetch_and_display_image()

# Run the Tkinter event loop
root.mainloop()
