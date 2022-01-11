import board
import displayio
import terminalio
from adafruit_display_text import label
import adafruit_displayio_ssd1306

displayio.release_displays()

try:
    i2c = board.I2C()
    display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
    display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=32)
    print("OLED Display initialized")
    OLED = True
except:
    print("OLED Display not found")
    OLED = False



def displayRows():
    screen = displayio.Group(max_size=4)
    for i in range(4):
        screen.append(label.Label(terminalio.FONT, text=rows[i], color=0xFFFFFF, x=0, y=i*8))
    display.show(screen)

def clear():
    screen = displayio.Group(max_size=4)
    for i in range(4):
        screen.append(label.Label(terminalio.FONT, text=" ", color=0xFFFFFF, x=0, y=i*8))
    display.show(screen)

def printTo(msg):
    if OLED:
        rows.pop(0)
        rows.append(msg)
        displayRows()



if OLED:
    rows = [" ", " ", " ", " "]
    clear()