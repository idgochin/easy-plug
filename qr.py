import qrcode
from tkinter import Tk, Label, Frame
from PIL import Image, ImageTk
import argparse
import sys

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Generate and display a QR code.")
parser.add_argument("--url", required=True, help="URL for the QR code")
parser.add_argument("--text", required=True, help="Text to display alongside the QR code")
args = parser.parse_args()

# Generate QR code
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data(args.url)
qr.make(fit=True)

# Create an image of the QR code
img = qr.make_image(fill_color="black", back_color="white")
img = img.convert("RGB")

# Create a tkinter root window
root = Tk()
root.attributes('-fullscreen', True)  # Make the window full-screen

# Get the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate the size of the square QR code to fit the screen
square_size = min(screen_width, screen_height) * 0.8  # 80% of screen size for better layout

# Resize the QR code image to a square
img = img.resize((int(square_size), int(square_size)), Image.Resampling.LANCZOS)
qr_image = ImageTk.PhotoImage(img)

# Create a frame to hold the text and QR code side by side
frame = Frame(root)
frame.pack(expand=True)

# Add the text to the frame
text_label = Label(frame, text=args.text, font=("Arial", 700))  # Adjust font size as needed
text_label.pack(side="left", padx=50)  # Add padding for spacing

# Add the QR code to the frame
qr_label = Label(frame, image=qr_image)
qr_label.pack(side="left")

# Bind Escape key to exit the window
# root.bind("<Escape>", lambda e: root.destroy())
root.bind("<Escape>", lambda e: sys.exit())

# Schedule the program to exit after 10 minutes (600,000 milliseconds)
root.after(60000, lambda: sys.exit())

# Run the tkinter main loop
root.mainloop()
