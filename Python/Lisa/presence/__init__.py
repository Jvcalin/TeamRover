from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))  #Make common library available


"""
The Presence loop maintains awareness of surroundings in a circular pattern
A circular array maintains a record of the readings from the prox sensors.
Fires alerts when about to collide with an object.
Is queried by the exec loop when it needs an open direction
"""