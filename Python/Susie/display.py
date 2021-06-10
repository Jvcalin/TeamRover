import board
import displayio
import terminalio
from adafruit_display_text import label

#TFT Display Size = 160x128

display = board.DISPLAY

# Set text, font, and color
text = "HELLO WORLD"
font = terminalio.FONT
color = 0x0000FF

# Create the text label
text_area = label.Label(font, text=text, color=color)

# Set the location
text_area.x = 30
text_area.y = 80

# Show it
display.show(text_area)

# Loop forever to prevent code from exiting
#while True:
#    pass