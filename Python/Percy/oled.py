import board
import displayio
import terminalio
from adafruit_display_text import label
import adafruit_displayio_ssd1306

displayio.release_displays()

i2c = board.I2C()
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=32)
print("OLED Display initialized")

class MyOLED:

    def __init__(self):
        self.rows = [" ", " ", " ", " "]
        self.clear()

    def displayRows(self):
        screen = displayio.Group(max_size=4)
        for i in range(4):
            screen.append(label.Label(terminalio.FONT, text=self.rows[i], color=0xFFFFFF, x=0, y=i*8))
        display.show(screen)

    def clear(self):
        screen = displayio.Group(max_size=4)
        for i in range(4):
            screen.append(label.Label(terminalio.FONT, text=" ", color=0xFFFFFF, x=0, y=i*8))
        display.show(screen)

    def print(self, msg):
        self.rows.pop(0)
        self.rows.append(msg)
        self.displayRows()



class MyPrint:

    def __init__(self):
        self.oled = MyOLED();

    def print(self,message):
        print(str(message))
        self.oled.print(str(message))




