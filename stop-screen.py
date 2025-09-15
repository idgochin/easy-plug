from tkinter import Tk, Label, Frame, font as tkFont, Canvas
import argparse
import sys

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Display text on fullscreen.")
parser.add_argument("--url", required=False, help="URL (not used, kept for compatibility)")
parser.add_argument("--text", required=True, help="Text to display")
args = parser.parse_args()

# Create a tkinter root window
root = Tk()
root.attributes('-fullscreen', True)
root.configure(bg='white')  # Set background color
root.config(cursor="none")

# Get the screen dimensions (typical 3.5" display is 480x320)
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Create main frame
main_frame = Frame(root, bg='white')
main_frame.pack(expand=True, fill='both')

# Determine layout orientation
if screen_width > screen_height:
    # Landscape layout (480x320) - use rotated text for better visibility
    layout = "landscape"
    
    # Create a canvas for rotated text
    canvas = Canvas(main_frame, bg='white', highlightthickness=0)
    canvas.pack(expand=True, fill='both')
    
    # Use very large font for 3.5" display visibility
    large_font = tkFont.Font(family="Arial", size=60, weight="bold")
    
    # Function to update text position and rotation
    def update_text_position(event=None):
        canvas.delete("all")
        canvas.create_text(
            canvas.winfo_width() // 2, 
            canvas.winfo_height() // 2,
            text=args.text, 
            font=large_font, 
            fill='black',
            angle=90  # 90 degrees rotation for landscape
        )
    
    canvas.bind('<Configure>', update_text_position)
    root.after(100, update_text_position)  # Initial positioning
    
else:
    # Portrait layout - standard text display
    layout = "portrait"
    
    # Use very large font for visibility on small screen
    large_font = tkFont.Font(family="Arial", size=60, weight="bold")
    
    # Create text label centered on screen
    text_label = Label(main_frame, 
                      text=args.text, 
                      font=large_font, 
                      bg='white', 
                      fg='black',
                      wraplength=screen_width-40, 
                      justify='center')
    text_label.pack(expand=True)

# Bind Escape key to exit (for testing)
root.bind("<Escape>", lambda e: sys.exit())

# Exit after 1 minute
root.after(60000, lambda: sys.exit())  # 1 minute = 60000 ms

# Run the tkinter main loop
root.mainloop()