import statistics as stat
import common.rovercollections as coll
# import equality as eq
import common.arrayshrinker as shrink
import common.influxdb as idb

"""
An "event" is a group of changes that happen on a time series graph
It ends when the values return to "normal" for a certain length of time
It begins either when the values go out of "normal" or from an external command
A monitor can only monitor one value over time.
The stopLength param is how many "quiet" ticks to record before making a "cut"

To account for outliers, we smooth the curve using a rolling average.
The smoothness param is the length of the rolling average.   (eg.  Avg of Last 7 ticks)

When an "event" occurs, it calls the callWhenEventOccurs function and returns a shape object of size shapeSize.

A shape object is just an array of slopes

Arrays Kept:
Raw - RollingArray of Length x
Smooth - RollingArray of rolling avgs
Deltas - RollingArray of deltas
"""


class EventMonitor:

    def __init__(self, name, size=100):
        self.stopLength = 10
        self.smoothness = 10
        self.onEventOccur = _publish
        self.monitorSize = size
        self.shapeSize = 25
        self.influxConn = idb.InfluxdbMeasurement("roger", name)
        # self.tupleSize = 0  # not a tuple

        # self.comparer = eq.RoundingEquality("medium", 3)
        self.raw = coll.RollingArray(self.monitorSize)
        self.smooth = coll.RollingArray(self.monitorSize)
        self.deltas = coll.RollingArray(self.monitorSize)

        self.recSize = 0
        self.quiet = 0
        self.recording = False

    def post(self, value):
        if isinstance(value, int) or isinstance(value, float):
            self._postNum(value)
        elif isinstance(value, tuple):
            self._postTuple(value)
        else:
            raise ValueError("value is not numeric or a tuple of numbers")

    def _postNum(self, value):
        self.raw.push(value)

        if len(self.raw.array) < self.smoothness:
            self.smooth.push(stat.mean(self.raw.array))
        else:
            self.smooth.push(stat.mean(self.raw.array[-1 * self.smoothness:]))

        if len(self.smooth.array) < 2:
            self.deltas.push(0)
        else:
            self.deltas.push(self.smooth.array[-1] - self.smooth.array[-2])

        if self.influxConn is not None:
            p = {"value": value, "smooth": self.smooth.array[-1], "delta": self.deltas.array[-1]}
            self.influxConn.post(p)

        if len(self.raw.array) == self.monitorSize:  # don't examine anything until we have a full rolling array
            self.analyze(value)

    def _postTuple(self, value):
        self.raw.push(value)

        if len(self.raw.array) < self.smoothness:
            self.smooth.push(_tupleMean(self.raw.array))
        else:
            self.smooth.push(_tupleMean(self.raw.array[-1 * self.smoothness:]))

        if len(self.smooth.array) < 2:
            a = []
            for _ in range(len(value)):
                a.append(0)
            self.deltas.push(tuple(a))
        else:
            a = []
            for i in range(len(value)):
                a.append(self.smooth.array[-1][i] - self.smooth.array[-2][i])
            self.deltas.push(tuple(a))

        if self.influxConn is not None and len(value) == 3:
            p = {"value_x": value[0], "smooth_x": self.smooth.array[-1][0], "delta_x": self.deltas.array[-1][0],
                 "value_y": value[1], "smooth_y": self.smooth.array[-1][1], "delta_y": self.deltas.array[-1][1],
                 "value_z": value[2], "smooth_z": self.smooth.array[-1][2], "delta_z": self.deltas.array[-1][2]}
            self.influxConn.post(p)

        if len(self.raw.array) == self.monitorSize:  # don't examine anything until we have a full rolling array
            self.analyze(value)

    def analyze(self, value):
        print(self.raw.getStdDev(), self.smooth.getStdDev())
        print(self.raw.getAvg(), self.smooth.getAvg())
        if self.recording:
            self.recSize += 1
            if self.trigger(value):
                self.quiet = 0
            else:
                if self.quiet > self.stopLength:
                    self.recording = False
                    self.quiet = 0
                    self.publishEvent()
                else:
                    self.quiet += 1
        else:
            if self.trigger(value):
                self.recSize = 1
                self.recording = True

    def trigger(self, value):
        if isinstance(value, int) or isinstance(value, float):
            return abs(self.smooth.getAvg() - value) > (2 * self.smooth.getStdDev())
        elif isinstance(value, tuple):
            avg = self.smooth.getAvg()
            stddev = self.smooth.getStdDev()
            for i in range(len(value)):
                if abs(avg[i] - value[i]) > (2 * stddev[i]):
                    return True
            return False
        else:
            raise ValueError("value is not numeric")

    # def quiet(self):
    #     return self.comparer.equals(self.deltas.array[-1], self.deltas.array[-2])

    def publishEvent(self):
        self.onEventOccur(shrink.shrink_num_array_to_size(self.deltas.array[self.recSize * -1:], self.shapeSize))


def _publish(shape):
    print(shape)


def _tupleMean(tuplearray):
    # each item in the array must be a same size tuple
    tuplesize = len(list(tuplearray[0]))
    totals = []
    for _ in range(tuplesize):
        totals.append(0)
    for i in range(len(tuplearray)):
        for j in range(tuplesize):
            totals[j] += tuplearray[i][j]
    for j in range(tuplesize):
        totals[j] /= len(tuplearray)
    return tuple(totals)
