import tkinter as tk
from PIL import Image, ImageTk
import requests
from io import BytesIO
import sys
import time

# Read the parameter (e.g., EZP000101 or EZP000102)
if len(sys.argv) != 2:
    print("Usage: python3 display-pay.py <parameter>")
    sys.exit(1)

parameter = sys.argv[1]
image_url = f"https://storage.googleapis.com/easy-plug-qr/qrcode/{parameter}.png"

# Function to fetch and display the image
def fetch_and_display_image():
    start_time = time.time()  # Record the start time
    retry_interval = 5  # Retry every 5 seconds
    timeout = 5 * 60  # Maximum wait time: 5 minutes

    while True:
        try:
            # Fetch the image from the URL
            response = requests.get(image_url)
            response.raise_for_status()  # Raise an error for bad status codes
            image_data = BytesIO(response.content)

            # Open the image using Pillow
            pil_image = Image.open(image_data)

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

        except requests.exceptions.RequestException as e:
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

# Fetch and display the image
fetch_and_display_image()

# Run the Tkinter event loop
root.mainloop()
