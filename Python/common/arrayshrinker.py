"""
The ArrayShrinker takes a 1 or multi-dimensional array and "pixelates" the array into a smaller array

This assumes each array in the array is the same size
"""


def shrink(array, factor):
    if not isinstance(array[0], list):
        if isinstance(array[0], tuple):
            return shrink_tuple_array(array, factor)
        else:
            return shrink_num_array(array, factor)
    else:
        i = 0
        small_array = []
        tarray = []
        for a in array:
            tarray.append(shrink(a, factor))
            i += 1
            if i == factor:
                small_array.append(merge_array(tarray, i))
                i = 0
                tarray.clear()
        if len(tarray) > 0:
            small_array.append(merge_array(tarray, i))
        return small_array


def shrink_num_array(array, factor):
    i = 0
    tsum = 0

    if isinstance(array[0], int):
        divfunc = int_div
    else:
        divfunc = float_div

    small_array = []
    for a in array:
        tsum += a
        i += 1
        if i == factor:
            small_array.append(divfunc(tsum, i))
            tsum = 0
            i = 0

    # add any remainder
    if tsum > 0:
        small_array.append(divfunc(tsum, i))

    return small_array


def shrink_tuple_array(array, factor):
    i = 0

    if isinstance(array[0][0], int):
        divfunc = int_div
    else:
        divfunc = float_div

    tsize = len(array[0])
    tsum = create_tuple_of_size(tsize)
    small_array = []
    for a in array:
        tsum = sum_tuples(tsum, a)
        i += 1
        if i == factor:
            small_array.append(tuple_div(tsum, i, divfunc))
            tsum = create_tuple_of_size(tsize)
            i = 0

    # add any remainder
    if tsum[0] > 0 and tsum[-1] > 0:
        small_array.append(tuple_div(tsum, i, divfunc))

    return small_array


# takes a 2 dimensional array of numbers
# returns an array of numbers
def merge_array(array, length):
    if isinstance(array[0][0], list):
        divfunc = merge_array
    elif isinstance(array[0][0], tuple):
        divfunc = tuple_div_alt
    elif isinstance(array[0][0], int):
        divfunc = int_div
    else:
        divfunc = float_div

    totals = []
    for a in array[0]:
        if isinstance(a, list):
            totals.append([])
        else:
            totals.append(0)
    ltotals = len(totals)
    for b in array:
        for i in range(ltotals):
            if isinstance(b[i], list):
                totals[i].append(b[i])
            elif isinstance(b[i], tuple):
                totals[i] = sum_tuples(totals[i], b[i])
            else:
                totals[i] += b[i]
    for i in range(ltotals):
        totals[i] = divfunc(totals[i], length)
    return totals


def get_dimensions(array):
    length = [len(array)]
    if isinstance(array[0], list):
        length += get_dimensions(array[0])
    return length


def int_div(a, b):
    return a // b


def float_div(a, b):
    return a / b


def sum_tuples(t1, t2):
    if len(t1) != len(t2):
        raise RuntimeError("tuples are not the same size")
    t = []
    for i in range(len(t1)):
        t.append(t1[i] + t2[i])
    return tuple(t)


def tuple_div(t1, size, divfunc):
    t = []
    for i in range(len(t1)):
        t.append(divfunc(t1[i], size))
    return tuple(t)


def tuple_div_alt(t1, size):
    if isinstance(t1[0], int):
        divfunc = int_div
    else:
        divfunc = float_div
    return tuple_div(t1, size, divfunc)


def create_tuple_of_size(size):
    t = []
    for i in range(size):
        t.append(0)
    return tuple(t)
