def add(n1, n2):
    return n1 + n2


def minus(n1, n2):
    return n1 - n2


def multiply(n1, n2):
    return n1 * n2


def divide(n1, n2):
    return n1/n2


def calculate(cal_function, n1, n2):
    return cal_function(n1, n2)


results = calculate(minus, 2, 2)
print(results)
