import board
import displayio
import terminalio
from adafruit_display_text import label
from adafruit_display_shapes.roundrect import RoundRect
from adafruit_display_shapes.triangle import Triangle

#TFT Display Size = 160x128

display = board.DISPLAY

"""
# define the controls
rect = RoundRect(30, 30, 100, 68, 5, fill=0x0, outline=0xFFFFFF, stroke=1)
screen.append(rect)
uptriangle = Triangle(80, 3, 44, 24, 116, 24, fill=0xADFF2F)
screen.append(uptriangle)
downtriangle = Triangle(80, 125, 44, 103, 116, 103, outline=0x2F4F4F)
screen.append(downtriangle)
lefttriangle = Triangle(3, 64, 24, 40, 24, 86, outline=0x2F4F4F)
screen.append(lefttriangle)
righttriangle = Triangle(157, 64, 134, 40, 134, 86, outline=0x2F4F4F)
screen.append(righttriangle)

robot_name_text = label.Label(terminalio.FONT, text="Percy", color=0xDC143C)
robot_name_text.x = 65
robot_name_text.y = 45
screen.append(robot_name_text)

mode1_text = label.Label(terminalio.FONT, text="[motors]", color=0xDCDCDC)
mode1_text.x = 60
mode1_text.y = 66
screen.append(mode1_text)

mode2_text = label.Label(terminalio.FONT, text="servos", color=0xC0C0C0)
mode2_text.x = 65
mode2_text.y = 83
screen.append(mode2_text)

display.show(screen)
"""


def show(up, down, left, right, robot, line1, line1highlight, line2, line2highlight):
    screen = displayio.Group(max_size=25)

    # define the controls
    rect = RoundRect(30, 30, 100, 68, 5, fill=0x0, outline=0xFFFFFF, stroke=1)
    screen.append(rect)

    if up:
        uptriangle = Triangle(80, 3, 44, 24, 116, 24, fill=0xADFF2F)
    else:
        uptriangle = Triangle(80, 3, 44, 24, 116, 24, outline=0x2F4F4F)
    screen.append(uptriangle)

    if down:
        downtriangle = Triangle(80, 125, 44, 103, 116, 103, fill=0xADFF2F)
    else:
        downtriangle = Triangle(80, 125, 44, 103, 116, 103, outline=0x2F4F4F)
    screen.append(downtriangle)

    if left:
        lefttriangle = Triangle(3, 64, 24, 40, 24, 86, fill=0xADFF2F)
    else:
        lefttriangle = Triangle(3, 64, 24, 40, 24, 86, outline=0x2F4F4F)
    screen.append(lefttriangle)

    if right:
        righttriangle = Triangle(157, 64, 134, 40, 134, 86, fill=0xADFF2F)
    else:
        righttriangle = Triangle(157, 64, 134, 40, 134, 86, outline=0x2F4F4F)
    screen.append(righttriangle)

    robot_name_text = label.Label(terminalio.FONT, text=robot, color=0xDC143C)
    robot_name_text.x = 65
    robot_name_text.y = 45
    screen.append(robot_name_text)

    if line1highlight:
        newline1 = "[{0}]".format(line1)
    else:
        newline1 = line1
    mode1_text = label.Label(terminalio.FONT, text=newline1, color=0xDCDCDC)
    mode1_text.x = 60
    mode1_text.y = 66
    screen.append(mode1_text)

    if line2highlight:
        newline2 = "[{0}]".format(line2)
    else:
        newline2 = line2
    mode2_text = label.Label(terminalio.FONT, text=newline2, color=0xC0C0C0)
    mode2_text.x = 65
    mode2_text.y = 83
    screen.append(mode2_text)

    display.show(screen)

"""

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


"""