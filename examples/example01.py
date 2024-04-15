import random

import snap4frame

snap4frame.init()


def calculate(x, y, z):
    return (x / z) * (z / y)


def f1():
    data = {"user": "You"}
    key = random.choice(["key", "user", "value"])
    value = data[key]
    print("Hello", value)
    x = 1
    y = 2
    z = 0
    return calculate(x, y, z)


def f2():
    f1()


def f():
    try:
        f2()
    except Exception as exp:
        raise exp


if __name__ == "__main__":
    f()
