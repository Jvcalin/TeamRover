import statistics as stat
import math
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

    def __init__(self, rover_name, measure_name, size=100, stop_length=10, smoothness=50, shape_size=50):
        self.rover = rover_name
        self.measure = measure_name
        self.stopLength = stop_length
        self.smoothness = smoothness
        self.onEventOccur = _publish
        self.monitorSize = size
        self.shapeSize = shape_size
        self.influxConn = None

        self.raw = coll.RollingArray(self.monitorSize)
        self.smooth = coll.RollingArray(self.monitorSize)
        self.deltas = coll.RollingArray(self.monitorSize)
        self.deltas_running_avg = 0
        self.deltas_running_stddev = 0

        self.recSize = 0
        self.quiet = 0
        self.recording = False

    def post(self, value):
        self.raw.push(value)

        if len(self.raw.array) < self.smoothness:
            self.smooth.push(stat.mean(self.raw.array))
        else:
            self.smooth.push(stat.mean(self.raw.array[-1 * self.smoothness:]))

        if len(self.smooth.array) < 2:
            if isinstance(value, int):
                self.deltas.push(0)
            else:
                self.deltas.push(0.0)
        else:
            self.deltas.push(self.smooth.array[-1] - self.smooth.array[-2])

        if self.influxConn is not None:
            p = {"value": value, "smooth": self.smooth.array[-1], "delta": self.deltas.array[-1]}
            self.influxConn.post(p)

        if len(self.raw.array) == self.monitorSize:  # don't examine anything until we have a full rolling array
            self.analyze(value)

    def startLog(self):
        self.influxConn = idb.InfluxdbMeasurement(self.rover, self.measure)

    def stopLog(self):
        self.influxConn = None

    def analyze(self, value):
        # print(self.raw.getStdDev(), self.smooth.getStdDev())
        # print(self.raw.getAvg(), self.smooth.getAvg())
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
            else:
                self._adjust_running_avg(value, self.monitorSize)

    def trigger(self, value):
        if isinstance(value, int) or isinstance(value, float):
            return abs(self.deltas_running_avg - value) > (3 * self.deltas_running_stddev)
        else:
            raise ValueError("value is not numeric")

    def publishEvent(self):
        pub = {"value": self.smooth.getAvg(),
               "shape": shrink.shrink_num_array_to_size(self.deltas.array[self.recSize * -1:], self.shapeSize)}
        self.onEventOccur(pub)

    def _adjust_running_avg(self, new_val, size):
        self.deltas_running_avg = ((self.deltas_running_avg * (size - 1)) * new_val) / size
        self.deltas_running_stddev = math.sqrt(((self.deltas_running_stddev ** 2 * (size - 1))
                                                + (new_val - self.deltas_running_avg) ** 2) / size)


class EventMonitorTuple(EventMonitor):

    def __init__(self, rover_name, measure_name, size=100, stop_length=10, smoothness=50, shape_size=50):
        self.deltas_running_avg_tuple = None
        self.deltas_running_stddev_tuple = None
        super().__init__(rover_name, measure_name, size, stop_length, smoothness, shape_size)

    def post(self, value):
        self.raw.push(value)
        print(value)

        tuplesize = len(value)
        if len(self.raw.array) < self.smoothness:
            self.smooth.push(self._tupleMean(self.raw.array))
        else:
            self.smooth.push(self._tupleMean(self.raw.array[-1 * self.smoothness:]))

        if len(self.smooth.array) < 2:
            a = []
            for i in range(tuplesize):
                if isinstance(value[i], int):
                    a.append(0)
                else:
                    a.append(0.0)
            self.deltas.push(tuple(a))
        else:
            a = []
            for i in range(tuplesize):
                a.append(self.smooth.array[-1][i] - self.smooth.array[-2][i])
            self.deltas.push(tuple(a))

        if self.deltas_running_avg_tuple is None:
            a = []
            for j in range(tuplesize):
                a.append(0)
            self.deltas_running_avg_tuple = tuple(a)
        if self.deltas_running_stddev_tuple is None:
            a = []
            for j in range(tuplesize):
                a.append(0)
            self.deltas_running_stddev_tuple = tuple(a)

        if self.influxConn is not None and tuplesize == 3 and len(self.smooth.array) > 2:
            avg = self.deltas_running_avg_tuple
            stddev = self.deltas_running_stddev_tuple
            p = {"value_x": value[0], "smooth_x": self.smooth.array[-1][0], "delta_x": self.deltas.array[-1][0]
                 , "delta_x_avg": avg[0], "delta_x.stddev": stddev[0]
                 # , "value_y": value[1], "smooth_y": self.smooth.array[-1][1], "delta_y": self.deltas.array[-1][1]
                 # , "delta_y_avg": avg[1], "delta_y.stddev": stddev[1]
                 # , "value_z": value[2], "smooth_z": self.smooth.array[-1][2], "delta_z": self.deltas.array[-1][2]
                 # , "delta_z_avg": avg[2], "delta_z.stddev": stddev[2]
                 }
            self.influxConn.post(p)

        if len(self.raw.array) == self.monitorSize:  # don't examine anything until we have a full rolling array
            self.analyze(self.deltas.array[-1])

    def trigger(self, value):
        if isinstance(value, tuple):
            avg = self.deltas_running_avg_tuple
            stddev = self.deltas_running_stddev_tuple
            for i in range(len(value)):
                if abs(avg[i] - value[i]) > (3 * stddev[i]):
                    print("Triggered!")
                    return True
            return False
        else:
            raise ValueError("value is not numeric")

    def _adjust_running_avg(self, new_val, size):
        b = []
        for i in range(len(new_val)):
            b.append(((self.deltas_running_avg_tuple[i] * (size - 1)) * new_val[i]) / size)
        self.deltas_running_avg_tuple = tuple(b)

        c = []
        for i in range(len(new_val)):
            c.append(math.sqrt(((self.deltas_running_stddev_tuple[i] ** 2 * (size - 1))
                                + (new_val[i] - self.deltas_running_avg_tuple[i]) ** 2) / size))
        self.deltas_running_stddev_tuple = tuple(c)

    @staticmethod
    def _tupleMean(tuple_array):
        # each item in the array must be a same size tuple
        tuplesize = len(list(tuple_array[0]))
        totals = []
        for _ in range(tuplesize):
            totals.append(0)
        for i in range(len(tuple_array)):
            for j in range(tuplesize):
                totals[j] += tuple_array[i][j]
        for j in range(tuplesize):
            totals[j] /= len(tuple_array)
        return tuple(totals)


def _publish(shape):
    print(shape)
