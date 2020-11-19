import statistics as stat
import rovercollections as coll
# import equality as eq
import arrayshrinker as shrink

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

    def __init__(self):
        self.stopLength = 10
        self.smoothness = 10
        self.onEventOccur = _publish
        self.monitorSize = 100
        self.shapeSize = 25

        # self.comparer = eq.RoundingEquality("medium", 3)
        self.raw = coll.RollingArray(self.monitorSize)
        self.smooth = coll.RollingArray(self.monitorSize)
        self.deltas = coll.RollingArray(self.monitorSize)

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
            self.deltas.push(0)
        else:
            self.deltas.push(self.smooth.array[-1] - self.smooth.array[-2])

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
        return abs(self.smooth.getAvg() - value) > (2 * self.smooth.getStdDev())

    # def quiet(self):
    #     return self.comparer.equals(self.deltas.array[-1], self.deltas.array[-2])

    def publishEvent(self):
        self.onEventOccur(shrink.shrink_num_array_to_size(self.deltas.array[self.recSize * -1:], self.shapeSize))


def _publish(shape):
    print(shape)


