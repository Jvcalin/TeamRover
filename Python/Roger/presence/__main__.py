import time
import presence


roger = presence.Presence()


while True:
    if roger.tick():
        break
    time.sleep(0.02)





