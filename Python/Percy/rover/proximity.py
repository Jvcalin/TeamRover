

arrSize = 10
arrPos = 0
running_array = [0] * arrSize


def push_value(value):
    global arrSize
    global arrPos
    global running_array
    running_array[arrPos] = value
    arrPos += 1
    if arrPos >= arrSize:
        arrPos = 0


def get_value():
    global running_array
    global arrSize
    return sum(running_array)/arrSize
