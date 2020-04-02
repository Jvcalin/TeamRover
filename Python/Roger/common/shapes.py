import statistics as stat

class GraphShape:    
    def __init__(self, sections):
        self.sections = sections
        self.size = 0
        for s in self.sections:
            self.size += s.size

    def compare(self, array, error = 0.25):
        i = 0
        for s in sections:
            d = GetSlope(array[i,s.size])
            i += s.size
            if d > (s.slope + error) or d < (s.slope - error):
                return False
        return True 



class GraphSections:
    def __init__(self, size, slope, average):
        self.size = size
        self.slope = slope
        self.average



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





array = [0, 1.4, 2.6, 3.7, 4.9]
print(GetSlope(array))