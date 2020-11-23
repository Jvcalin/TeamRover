import statistics as stat


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
        if isinstance(self.array[0], int) or isinstance(self.array[0], float):
            return stat.mean(self.array)
        elif isinstance(self.array[0], tuple):
            return _apply_aggregate_function_to_tuple_array(stat.mean, self.array)

    def getRange(self):
        if isinstance(self.array[0], int) or isinstance(self.array[0], float):
            return max(self.array) - min(self.array)
        elif isinstance(self.array[0], tuple):
            return _apply_aggregate_function_to_tuple_array(lambda x: max(x) - min(x), self.array)
        # return max(self.array) - min(self.array)

    def getStdDev(self):
        if isinstance(self.array[0], int) or isinstance(self.array[0], float):
            return stat.stdev(self.array)
        elif isinstance(self.array[0], tuple):
            return _apply_aggregate_function_to_tuple_array(stat.stdev, self.array)

    def getMedian(self):
        if isinstance(self.array[0], int) or isinstance(self.array[0], float):
            return stat.median(self.array)
        elif isinstance(self.array[0], tuple):
            return _apply_aggregate_function_to_tuple_array(stat.median, self.array)
        # return stat.median(self.array)

    def getVariance(self):
        if isinstance(self.array[0], int) or isinstance(self.array[0], float):
            return stat.variance(self.array)
        elif isinstance(self.array[0], tuple):
            return _apply_aggregate_function_to_tuple_array(stat.variance, self.array)
        # return stat.variance(self.array)

    def getPVariance(self):
        if isinstance(self.array[0], int) or isinstance(self.array[0], float):
            return stat.pvariance(self.array)
        elif isinstance(self.array[0], tuple):
            return _apply_aggregate_function_to_tuple_array(stat.pvariance, self.array)
        # return stat.pvariance(self.array)

    def getTrend(self, size):
        if isinstance(self.array[0], int) or isinstance(self.array[0], float):
            return stat.stdev(self.array)
        elif isinstance(self.array[0], tuple):
            return _apply_aggregate_function_to_tuple_array(lambda x: self._getTrend(x, size), self.array)


def _getTrend(array, size):
    deltas = []
    if size > len(array):
        Size = len(array)
    else:
        Size = size
    for x in range(len(array)-Size, len(array)):
        if x > 0:
            delta = array[x] - array[x-1]
            deltas.append(delta)
    if len(deltas) == 0:
        return 0
    else:
        return stat.mean(deltas)


def _transpose_matrix(mat):
    return [[mat[j][i] for j in range(len(mat))] for i in range(len(mat[0]))]


def _apply_aggregate_function_to_tuple_array(func, array):
    tarray = _transpose_matrix(array)
    t = []
    for i in tarray:
        t.append(func(i))
    return tuple(t)

