"""
This module performs equality checks using resolution adjustment

Rounding (by 2) is done by bit shifting (int divide by 2) the two operands and then making a comparison.

256 = 2^8 = 100,000,000
128 = 2^7 = 10,000,000
64 = 2^6 = 1,000,000
32 = 2^5 = 100,000
16 = 2^4 = 10,000
8 = 2^3 = 1,000
4 = 2^2 = 100
2 = 2^1 = 10
1 = 2^0 = 1

255 = 11,111,111
135 = 128 + 0 + 0  + 0 + 4 + 2 + 1  => 01,000,111
175 = 128 + 0 + 32 + 8 + 4 + 2 + 1  => 01,011,111

n = number of binary digits of highest number + 1 -> 256 -> n=8
r = resolution
    -> exact = exact match, only 1 match  r = n
    -> high = almost exact match, few matches r = 3/4 n
    -> low = fair match, lots of matches r = 1/4 n
    -> medium = good match, medium # of matches r = 1/2 n

a ?= b

a / 2^(n-r) ?= b / 2^(n-r)  -> integer division -> discard remainder
a >> (n-r-1) ?= b >> (n-r-1)

135 ?= 175

n = 8
Exact: a != b

r = 7 => 128 buckets of 2
135 / 2 ?= 175 / 2

High: r = 6 => 64 buckets of 4
135 / 4 ?= 175 / 4
33 != 43

r = 5 => 32 buckets of 8
135 / 8 ?= 135 / 8

Medium: r = 4 => 16 buckets of 16
135 / 16 ?= 175 / 16
8 != 10

r = 6 => 8 buckets of 32
135 / 32 ?= 175 / 32
4 != 5

Low: r = 2 => 4 buckets of 64   0 to 63, 64 to 127, 128 to 191, 192 to 255
135 / 64 ?= 175 / 64
2 = 2

"""


class RoundingEquality:

    def __init__(self, resolution, tolerance=0):
        self.n = 0
        self.r = 0
        self.resolution = resolution
        self.tolerance = tolerance  # tolerance is the percentage of mismatches allowed in the array
        self.count = 0
        self.fails = 0

    def equals(self, num1, num2):
        self.n = find_n(greater(max_value(num1), max_value(num2)))
        self.r = resolution_to_number(self.n, self.resolution)
        self.count = 0
        self.fails = 0
        if self.__eval_equals(num1, num2):
            return True
        else:
            return (self.fails / self.count) < (self.tolerance / 100)

    def __eval_equals(self, num1, num2):
        print("num1={} num2={} n={} r={}".format(num1, num2, self.n, self.r))
        if (type(num1) != type(num2)) and not ((isinstance(num1, int) or isinstance(num1, float)) and (isinstance(num2, int) or isinstance(num2, float))):
            raise RuntimeError("Operands must be the same type")

        if isinstance(num1, list):
            # in a list, all items must be "equal" to return equal
            if len(num1) != len(num2):  # if the lists are different lengths, raise error
                raise RuntimeError("Lists must be the same size")
            return_value = True
            for i in range(len(num1)):
                if not self.__eval_equals(num1[i], num2[i]):
                    if self.tolerance == 0:
                        return False  # if tolerance is 0, don't bother calculating the rest of the array
                    else:
                        return_value = False
            return return_value

        elif isinstance(num1, tuple):
            # to compare tuples, each value must be equal to the corresponding value in the other
            self.count += 1
            if compare_tuples(num1, num2):
                return True
            else:
                for i in range(len(num1)):
                    if abs(num1[i] - num2[i]) >= 2 ** (self.n - self.r):
                        self.fails += 1
                        return False
                return True
        elif isinstance(num1, int) or isinstance(num1, float):
            self.count += 1
            if num1 == num2:
                return True
            else:
                if abs(num1 - num2) < 2**(self.n - self.r):   # this compensates for two close numbers straddling
                    return True
                else:
                    self.fails += 1
                    return False
                # Obsolete:
                # if num1 < 0:  # bit shifting comparison requires positive numbers
                #     num1 *= -1
                #     num2 *= -1
                # return (num1 >> self.n - (self.r + 1)) == (num2 >> self.n - (self.r + 1))

        else:
            raise RuntimeError("Invalid types - must be list of ints or int")

    def equals_low(self, num1, num2):
        self.resolution = "low"
        self.r = resolution_to_number(self.n, "low")
        return self.equals(num1, num2)

    def equals_medium(self, num1, num2):
        self.resolution = "medium"
        self.r = resolution_to_number(self.n, "medium")
        return self.equals(num1, num2)

    def equals_high(self, num1, num2):
        self.resolution = "high"
        self.r = resolution_to_number(self.n, "high")
        return self.equals(num1, num2)


# n is the first power of 2 greater than num
def find_n(num):
    n = 1
    while num > 2 ** n:
        n += 1
    return n


# returns whichever is greater
def greater(num1, num2):
    if num1 > num2:
        return num1
    else:
        return num2


# returns whichever is lesser
def lesser(num1, num2):
    if num1 < num2:
        return num1
    else:
        return num2


# returns a number from resolution
def resolution_to_number(n, resolution):
    if resolution == "exact":
        return n
    elif resolution == "low":
        return n // 4
    elif resolution == "medium":
        return n // 2
    elif resolution == "high":
        return n // 4 * 3
    else:
        raise RuntimeError("invalid resolution: " + resolution)


# returns the maximum value
def max_value(array):
    if isinstance(array, int) or isinstance(array, float):
        return array
    else:
        maximum = 0
        for i in array:
            if isinstance(i, list):
                imax = max_value(i)
                if imax > maximum:
                    maximum = imax
            elif isinstance(i, tuple):
                imax = max_value(list(i))
                if imax > maximum:
                    maximum = imax
            else:
                if i > maximum:
                    maximum = i
        return maximum


def compare_tuples(num1, num2):
    if len(num1) == len(num1):
        for i in range(len(num1)):
            if num1[i] != num2[i]:
                return False
        return True
    else:
        raise RuntimeError("tuples don't have the same number of values")