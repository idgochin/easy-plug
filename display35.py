#!/usr/bin/env python3
"""
Full black screen for Raspberry Pi 4 with 3.5 inch display
True fullscreen mode - covers everything including taskbar
"""

import qrcode
from tkinter import Tk, Label, Frame, font as tkFont
from PIL import Image, ImageTk, ImageFont, ImageDraw
import argparse
import sys

# Create a tkinter root window
root = Tk()
root.attributes('-fullscreen', True)
root.configure(bg='black')  # Set background color
root.attributes('-topmost', True)
root.config(cursor="none")

# # Grab all keyboard and mouse input (optional - makes it harder to accidentally exit)
root.grab_set()

# Press Escape or q to exit
# Bind Escape key to exit
root.bind("<Escape>", lambda e: sys.exit())


# Start the main loop
root.mainloop()

