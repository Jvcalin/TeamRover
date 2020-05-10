import statistics as stat

class GraphShape:    
    def __init__(self, sections):
        self.sections = sections
        self.size = 0
        for s in self.sections:
            self.size += s.size

    def compare(self, array):
        i = 0
        for s in self.sections:
            d = GetSlope(array[i:s.size])
            i += s.size
            if d > (s.slope + s.error) or d < (s.slope - s.error): 
                return False
        return True 



class GraphSection:
    def __init__(self, size, slope, average, error):
        self.size = size
        self.slope = slope
        self.average = average
        self.error = error


def GetSlope(array):
    #array of numbers
    if len(array) == 0:
        return 0
    deltas = []
    for x in range(1,len(array)-1):
        delta = array[x] - array[x-1]
        deltas.append(delta)
    if len(deltas) == 0:
        return 0
    else:
        return stat.mean(deltas)    





# array = [0, 1.4, 2.6, 3.7, 4.9]
# print(GetSlope(array))