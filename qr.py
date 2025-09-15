# import qrcode
# from tkinter import Tk, Label, Frame
# from PIL import Image, ImageTk
# import argparse
# import sys

# # Parse command-line arguments
# parser = argparse.ArgumentParser(description="Generate and display a QR code.")
# parser.add_argument("--url", required=True, help="URL for the QR code")
# parser.add_argument("--text", required=True, help="Text to display alongside the QR code")
# args = parser.parse_args()

# # Generate QR code
# qr = qrcode.QRCode(
#     version=1,
#     error_correction=qrcode.constants.ERROR_CORRECT_L,
#     box_size=10,
#     border=4,
# )
# qr.add_data(args.url)
# qr.make(fit=True)

# # Create an image of the QR code
# img = qr.make_image(fill_color="black", back_color="white")
# img = img.convert("RGB")

# # Create a tkinter root window
# root = Tk()
# root.attributes('-fullscreen', True)  # Make the window full-screen

# # Get the screen width and height
# screen_width = root.winfo_screenwidth()
# screen_height = root.winfo_screenheight()

# # Calculate the size of the square QR code to fit the screen
# square_size = min(screen_width, screen_height) * 0.8  # 80% of screen size for better layout

# # Resize the QR code image to a square
# img = img.resize((int(square_size), int(square_size)), Image.Resampling.LANCZOS)
# qr_image = ImageTk.PhotoImage(img)

# # Create a frame to hold the text and QR code side by side
# frame = Frame(root)
# frame.pack(expand=True)

# # Add the text to the frame
# text_label = Label(frame, text=args.text, font=("Arial", 700))  # Adjust font size as needed
# text_label.pack(side="left", padx=50)  # Add padding for spacing

# # Add the QR code to the frame
# qr_label = Label(frame, image=qr_image)
# qr_label.pack(side="left")

# # Bind Escape key to exit the window
# # root.bind("<Escape>", lambda e: root.destroy())
# root.bind("<Escape>", lambda e: sys.exit())

# # Schedule the program to exit after 10 minutes (600,000 milliseconds)
# root.after(60000, lambda: sys.exit())

# # Run the tkinter main loop
# root.mainloop()

import qrcode
from tkinter import Tk, Label, Frame, font as tkFont
from PIL import Image, ImageTk, ImageFont, ImageDraw
import argparse
import sys

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Generate and display a QR code.")
parser.add_argument("--url", required=True, help="URL for the QR code")
parser.add_argument("--text", required=True, help="Text to display alongside the QR code")
args = parser.parse_args()

# Generate QR code with higher error correction for small displays
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_M,  # Medium error correction
    box_size=6,  # Smaller box size for 3.5" display
    border=2,    # Smaller border to save space
)
qr.add_data(args.url)
qr.make(fit=True)

# Create an image of the QR code
img = qr.make_image(fill_color="black", back_color="white")
img = img.convert("RGB")

# Create a tkinter root window
root = Tk()
root.attributes('-fullscreen', True)
root.configure(bg='white')  # Set background color
root.config(cursor="none")

# Get the screen dimensions (typical 3.5" display is 480x320)
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate optimal layout for 3.5" display
# Assume landscape orientation (480x320)
if screen_width > screen_height:
    # Landscape layout - QR code on left, text on right
    qr_size = int(screen_height * 0.8)  # 80% of height
    text_width = screen_width - qr_size - 40  # Remaining width minus padding
    layout = "landscape"
else:
    # Portrait layout - text on top, QR code below
    qr_size = int(screen_width * 0.8)  # 80% of width
    text_height = screen_height - qr_size - 40  # Remaining height minus padding
    layout = "portrait"

# Resize the QR code image
img = img.resize((qr_size, qr_size), Image.Resampling.LANCZOS)
qr_image = ImageTk.PhotoImage(img)

# Create main frame
main_frame = Frame(root, bg='white')
main_frame.pack(expand=True, fill='both')

if layout == "landscape":
    # Landscape layout
    # QR code on the left
    qr_label = Label(main_frame, image=qr_image, bg='white')
    qr_label.pack(side="left", padx=(20, 10), pady=20)
    
    # Text on the right with large font and -90 degree rotation using Canvas
    text_frame = Frame(main_frame, bg='white')
    text_frame.pack(side="right", fill='both', expand=True, padx=(10, 20), pady=20)
    
    # Create a canvas for rotated text
    from tkinter import Canvas
    canvas = Canvas(text_frame, bg='white', highlightthickness=0)
    canvas.pack(expand=True, fill='both')
    
    # Use tkinter's font system for reliable large fonts
    large_font = tkFont.Font(family="Arial", size=60, weight="bold")  # Very large font
    
    # Add text to canvas and rotate it
    canvas.create_text(
        canvas.winfo_reqwidth() // 2, 
        canvas.winfo_reqheight() // 2,
        text=args.text, 
        font=large_font, 
        fill='black',
        angle=90  # 180 degrees rotation (upside down)
    )
    
    # Update canvas after it's drawn
    def update_text_position(event=None):
        canvas.delete("all")
        canvas.create_text(
            canvas.winfo_width() // 2, 
            canvas.winfo_height() // 2,
            text=args.text, 
            font=large_font, 
            fill='black',
            angle=90  # 180 degrees rotation (upside down)
        )
    
    canvas.bind('<Configure>', update_text_position)
    root.after(100, update_text_position)  # Initial positioning
    
else:
    # Portrait layout
    # Text on top with large font
    text_frame = Frame(main_frame, bg='white', height=text_height)
    text_frame.pack(side="top", fill='x', padx=20, pady=(20, 10))
    text_frame.pack_propagate(False)
    
    # Use large tkinter font
    large_font = tkFont.Font(family="Arial", size=48, weight="bold")  # Very large font
    
    text_label = Label(text_frame, text=args.text, font=large_font, 
                      bg='white', wraplength=screen_width-40, justify='center')
    text_label.pack(expand=True)
    
    # QR code below
    qr_label = Label(main_frame, image=qr_image, bg='white')
    qr_label.pack(side="bottom", padx=20, pady=(10, 20))

# Bind Escape key to exit
root.bind("<Escape>", lambda e: sys.exit())

# Exit after 1 minutes
root.after(60000, lambda: sys.exit())  # 1 minutes = 60000 ms

# Run the tkinter main loop
root.mainloop()