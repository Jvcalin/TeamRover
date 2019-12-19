import math as math

class Space2D:
    
    def __init__(self):
        self.list = []

    def find(self, square):
        for x in self.list:
            if x == square:
                return x
        return None

    def add(self, square):
        x = self.find(square)
        if x is None:
            self.list.append(square)
        else:
            x.increment()

    def addVector(self, origin, length, angle):
        #calculate x and y distances
        #angle is in degrees
        x = math.cos(math.radians(angle)) * length
        y = math.sin(math.radians(angle)) * length
        print(round(x),round(y))
        self.add(GridSquare(round(x),round(y)))

    def shift(self, x1, y1):
        for i in self.list:
            i.x += x1
            i.y += y1



class GridSquare:

    def __init__ (self, x, y):
        self.x = x
        self.y = y
        self.weight = 1

    def __eq__ (self, square):
        return (self.x == square.x) and (self.y == square.y)

    def increment(self):
        self.weight += 1

    def getWeight(self):
        return self.weight


"""
mylist = [GridSquare(1,0), GridSquare(2,4), GridSquare(2,-3)]

if mylist[0] == GridSquare(1,0):
    print("hey")
"""

space = Space2D()
space.add(GridSquare(0,0))
space.addVector((0,0), 3, -45)




