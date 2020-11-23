"""
Serialize various objects to json
"""
import importlib

def toJSON(item):
    if isinstance(item, list):
        s = ""
        for i in item:
            s += toJSON(i) + ","
        return "[" + s[:-1] + "]"
    elif isinstance(item, dict):
        s = ""
        for i in item.keys():
            s += "\"" + i + "\":" + toJSON(item[i]) + ","
        return "{\"name\":\"dict\", \"value\": {" + s[:-1] + "}}"
    elif isinstance(item, tuple):
        return "{\"name\":\"tuple\", \"value\": " + toJSON(list(item)) + "}"
    elif isinstance(item, int):
        return str(item)
    elif isinstance(item, float):
        return str(item)
    elif isinstance(item, str):
        return "\"" + item + "\""
    elif callable(item):
        pass
    elif isinstance(item, TypeHolder):
        return "{\"name\":\"" + item.name + "\", \"module\":\"" + item.module + "\", \"value\": " + toJSON(item.value) + "}"
    else:
        s = ""
        try:
            s = item.toJSON()  # if the item has a defined toJSON method, use that
        except AttributeError:
            try:
                d = item.__dict__  # convert object into a dict
                for i in d.keys():
                    s += "\"" + i + "\":" + toJSON(d[i]) + ","
                s = "{" + s[:-1] + "}"
            except AttributeError:
                s = "\"" + str(item) + "\""

        return "{\"name\":\"" + type(item).__name__ + "\", \"module\":\"" + type(item).__module__ + "\", \"value\": " + s + "}"


def fromJSON(json):
    json = __cleanJSON(json)
    if json == "":
        return None
    elif json[0] == "{" and json[-1] == "}":
        r, s = __getDict(json)
        return r
    elif json[0] == "[" and json[-1] == "]":
        r, s = __getList(json)
        return r
    else:
        raise SyntaxError("invalid json")


def __cleanJSON(json):
    # remove any spaces (except inside quotes) and any whitespace chars
    quotes = []
    newjson = ""
    for i in range(len(json)):
        if json[i] == '"':
            if len(quotes) > 0 and quotes[-1] == "d":
                quotes.pop()
            else:
                quotes.append("d")
        elif json[i] == "'":
            if len(quotes) > 0 and quotes[-1] == "s":
                quotes.pop()
            else:
                quotes.append("s")
        elif json[i] in [' ', '\n', '\r', '\t', '\f']:
            if len(quotes) == 0:
                continue
        newjson += json[i]
    return newjson


def __getObject(json):
    if json[0] == "{":
        return __getDict(json)
    elif json[0] == "[":
        return __getList(json)
    elif json[0] == '"':
        return __getString(json)
    elif json[0].isdecimal() or json[0] == '-':
        return __getNumber(json)
    elif json[0:4].lower() == "true" or json[0:5].lower() == "false":
        return __getBool(json)
    else:
        raise SyntaxError("Invalid object")


def __getDict(json):
    theDict = {}
    if json[0] == '{':
        json = json[1:]
    label, item, json = __getProperty(json)
    theDict[label] = item
    while json[0] == ',':
        json = json[1:]
        label, item, json = __getProperty(json)
        theDict[label] = item
    if json[0] == '}':
        json = json[1:]
        theDict = __evaluateDict(theDict)
        return theDict, json
    else:
        raise SyntaxError("Invalid Dict")


def __evaluateDict(theDict):
    try:
        if theDict["name"] == "dict":
            return theDict
        elif theDict["name"] == "tuple":
            return tuple(theDict.value)
        else:
            # instantiate the class here
            t = TypeHolder(theDict["name"], theDict["value"], theDict["module"])
            return t
    except KeyError:
        return theDict


def __getList(json):
    if json[0] == '[':
        json = json[1:]
    theList = []
    item, json = __getObject(json)
    theList.append(item)
    while json[0] == ',':
        json = json[1:]
        item, json = __getObject(json)
        theList.append(item)
    if json[0] == ']':
        json = json[1:]
        return theList, json
    else:
        raise SyntaxError("Invalid List")



def __getString(json):
    t, json = __getToEndChar(json)
    s = __parseString(t)
    return s, json


def __getNumber(json):
    s, json = __getToEndChar(json)
    n = __parseNumber(s)
    return n, json


def __getBool(json):
    s, json = __getToEndChar(json)
    b = __parseNumber(s)
    return b, json

#
# def __getList(json):
#     json, c1 = __trim(json)
#     item, cursor = __getObject(json)
#     length = cursor
#     thelist = [item]
#     while item is not None and json[cursor] == ',':
#         json, c = __trim(json[cursor + 1:])
#         item, cursor = __getObject(json)
#         length += cursor + c + 1
#         thelist.append(item)
#     if json[cursor] == ']':
#         return thelist, length + c1 + 1
#     else:
#         raise SyntaxError("invalid list")
#

# def __getDict(json):
#     json, c1 = __trim(json)
#     theDict = {}
#     key, item, cursor = __getProperty(json)
#     length = cursor
#     while json[cursor] == " ":
#         cursor += 1
#     theDict[key] = item
#     while item is not None and json[cursor] == ',':
#         json, c = __trim(json[cursor + 1:])
#         key, item, cursor = __getProperty(json)
#         while json[cursor] == " ":
#             cursor += 1
#         length += cursor + c + 1
#         theDict[key] = item
#     if json[cursor] == '}':
#         return theDict, length + c1 + 1
#     else:
#         raise SyntaxError("invalid dict")


# def __getObject(json):
#     json, c = __trim(json)
#     if len(json) == 0:
#         return None
#     elif json[0] == '{':
#         d, e = __getDict(json[1:])
#         try:
#             if d.name == "dict":
#                 return d.value, e + c + 1
#             elif d.name == "tuple":
#                 return tuple(d.value), e + c + 1
#             else:
#                 # instantiate the class here
#                 t = TypeHolder(d.name, d.module, d.value)
#                 # t = type(d.name, TypeHolder, d.value)()
#                 return t, e + c + 1
#         except AttributeError:
#             return d, e + c + 1
#     elif json[0] == '[':
#         l, e = __getList(json[1:])
#         return l, e + c + 1
#     elif json[0] == '\"':
#         w, e = __getToEndChar(json)
#         w, c1 = __trim(w)
#         s = __parseString(w)
#         return s, e + c
#     elif json[0].isnumeric():
#         w, e = __getToEndChar(json)
#         w, c1 = __trim(w)
#         n = __parseNumber(w)
#         return n, e + c
#     else:
#         raise SyntaxError("invalid object")


def __getToEndChar(json):
    for i in range(len(json)):
        if json[i] in [',', '}', ']', ':']:
            break
    return json[:i], json[i:]

# def __getProperty(json):
#     # "<name>":object
#     json, c = __trim(json)
#     # property must always start with the label
#     v = json.find(':')
#     if v >= 0:
#         label = __parseString(json[:v], True)
#         item, length = __getObject(json[v+1:])
#         return label, item, v + length + c + 1
#     else:
#         raise SyntaxError("not a valid property")


def __getProperty(json):
    label, json = __getToEndChar(json)
    label = __parseString(label, True)
    if json[0] == ":":
        json = json[1:]
    else:
        raise SyntaxError("not a valid property")
    value, json = __getObject(json)
    return label, value, json


def __parseString(json, alphaonly=False):
    # "xxx" or "xxx xxx"
    if json[0] == '\"' and json[-1] == '\"':
        s = json[1:-1]
        if alphaonly:
            if s.replace('_', "").isalnum():
                return s
        else:
            return s
    raise SyntaxError("invalid string")


def __parseNumber(json):
    # 123 or 12.3
    if json[0] == '-':
        neg = -1
        json = json[1:]
    else:
        neg = 1
    if json.isalpha():
        if json.lower() == "true":
            return True
        elif json.lower() == "false":
            return False
        else:
            raise SyntaxError("invalid number")
    try:
        if '.' in json:
            return float(json) * neg
        else:
            return int(json) * neg
    except ValueError:
        raise SyntaxError("invalid number")


# def __trim(string, count=0):
#     if string[0] in [' ', '\n', '\r', '\t', '\f']:
#         return __trim(string[1:], count + 1)
#     elif string[-1] in [' ', '\n', '\r', '\t', '\f']:
#         return __trim(string[:-1], count + 1)
#     else:
#         return string, count


class TypeHolder:
    def __init__(self, typename, value, modulename = ""):
        self.name = typename
        self.module = modulename
        self.value = value

