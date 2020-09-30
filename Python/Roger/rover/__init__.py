from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))  #Make common library available


"""
The rover loop is the main interface to the Matrix Creator
It maintains a record of and status of the IMU 
-- senses forward, backward movement
-- rotation
-- tipping
Can receive commands to control the led matrix

Temp sensor
Light sensor
IR sensor?
IR signals
"""