import random

import snap4frame
import snap4frame.processor
import snap4frame.processor.kit

snap4frame.setup_handler(
    "default",
    [
        snap4frame.processor.kit.FileSaveProcessor(
            create_path=True,
            exists_ok=True,
        ),
    ],
)
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
        snap4frame.emit(exp)
        raise exp


if __name__ == "__main__":
    f()
