import tkinter as tk
from PIL import Image, ImageTk
import requests
from io import BytesIO

# URL of the image in Google Cloud Storage
image_url = "https://storage.googleapis.com/easy-plug-qr/qrcode/EZP000101.png"

# Function to fetch and display the image
def fetch_and_display_image():
    try:
        # Fetch the image from the URL
        response = requests.get(image_url)
        response.raise_for_status()  # Raise an error for bad status codes
        image_data = BytesIO(response.content)

        # Open the image using Pillow
        pil_image = Image.open(image_data)

        # Calculate new dimensions (30% of original)
        original_width, original_height = pil_image.size
        new_width = int(original_width * 2.3)
        new_height = int(original_height * 2.3)

        # Resize the image to 30% of its original size
        pil_image = pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # Convert to a format suitable for Tkinter
        tk_image = ImageTk.PhotoImage(pil_image)

        # Create a label in Tkinter to display the image
        label = tk.Label(root, image=tk_image, bg="black")
        label.image = tk_image  # Keep a reference to avoid garbage collection
        label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    except Exception as e:
        print(f"Error fetching or displaying the image: {e}")

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
