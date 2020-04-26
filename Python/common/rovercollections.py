import statistics as stat
import collections 


class CircularArray:

    def __init__(self, size, factory):
        self.circarray = []
        self.currentIndex = 0
        for x in range(size):
            item = factory()
            self.circarray.append(item)

    def __iter__(self):       
        return self

    def __next__(self):
        x = self.circarray[self.currentIndex]
        if self.currentIndex >= len(self.circarray):
            self.currentIndex = 0
        else:
            self.currentIndex += 1
        return x

    def GetArray(self, startFrom):
        return self.circarray[startFrom:] + self.circarray[:startFrom]

    def GetItem(self, startFrom, index):
        i = index + startFrom
        if i > len(self.circarray):
            i -= len(self.circarray)
        return self.circarray[i]


class RollingArray:
    # This array will stay at one size
    # When an item is pushed on, the bottom one is discarded
    def __init__(self, size):
        self.array = [] #collections.deque()
        self.index = 0
        self.size = size

    def push(self, item):
        self.array.append(item)
        while len(self.array) > self.size:
            del self.array[0]
            #self.array.popleft()

    def weight(self):
        return len(self.array)

    def get(self):
        return self.array
        #arr = []
        #for s in self.array:
        #    arr.append(s)
        #return arr

    def getAvg(self):
        return stat.mean(self.array)

    def getRange(self):
        return max(self.array) - min(self.array)

    def getStdDev(self):
        return stat.stdev(self.array)

    def getMedian(self):
        return stat.median(self.array)

    def getVariance(self):
        return stat.variance(self.array)

    def getPVariance(self):
        return stat.pvariance(self.array)

    def getTrend(self, size):
        deltas = []
        if size > len(self.array):
            Size = len(self.array)
        else:
            Size = size
        for x in range(len(self.array)-Size, len(self.array)):
            if x > 0:
                delta = self.array[x] - self.array[x-1]
                deltas.append(delta)
        if len(deltas) == 0:
            return 0
        else:
            return stat.mean(deltas)

            
