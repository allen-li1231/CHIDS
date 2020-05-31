"""
@Author: Allen Li   5/22/2020
"""
import re
import numpy as np


class numInterval(float):
    def __new__(cls, n):
        if isinstance(n, str):
            n = n.replace(" ", '')
            check = re.findall(r"^([<>]?=?)([+-]?\.?\d+\.?\d*)$", n)
            if check:
                return super().__new__(cls, check[0][1])
            else:
                raise ValueError(f"could not convert string to numInterval: '{n}'")
        elif isinstance(n, (int, float, np.dtype)):
            return super().__new__(cls, n)

    def __init__(self, n):
        if isinstance(n, str):
            n = n.replace(" ", '')
            check = re.findall(r"^([<>]?=?)([+-]?\.?\d+\.?\d*)$", n)
            if check:
                self._symbol, self._n = check[0]
                self._n = float(self._n)
            else:
                raise ValueError(f"could not convert string to numInterval: '{n}'")
        else:
            self._symbol = ''
            self._n = float(n)

        if self._symbol:
            self.is_range = True
        else:
            self.is_range = False

        super().__init__()

    def __add__(self, other):
        if isinstance(other, numInterval):
            if self._symbol == other._symbol:
                return numInterval(f"{self._symbol}{self._n + other._n}")

        if isinstance(other, (int, float, np.dtype)):
            return numInterval(f"{self._symbol}{other + self._n}")

        raise TypeError(f"unsupported operand type(s) for +: '{type(self)}' and '{type(other)}'")

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        return numInterval(f"{self._symbol}{self._n - other}")

    def __rsub__(self, other):
        return numInterval(f"{self._symbol}{other - self._n}")

    def __mul__(self, other):
        return numInterval(f"{self._symbol}{self._n * other}")

    def __rmul__(self, other):
        return self.__mul__(other)

    def __floordiv__(self, other):
        return numInterval(f"{self._symbol}{self._n // other}")

    def __truediv__(self, other):
        return numInterval(f"{self._symbol}{self._n / other}")

    def __rfloordiv__(self, other):
        return numInterval(f"{self._symbol}{other // self._n}")

    def __rtruediv__(self, other):
        return numInterval(f"{self._symbol}{other / self._n}")

    def __hash__(self):
        return int(self._n)

    def __eq__(self, other):
        if isinstance(other, numInterval):
            if other._symbol == self._symbol and other._n == self._n:
                return True
        if self.is_range:
            return False
        else:
            return super(numInterval, self).__eq__(other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other):
        if isinstance(other, numInterval):
            if self._symbol in ["<=", "<"] and other._symbol in [">=", ">"]:
                return False

        return not self.__le__(other)

    def __ge__(self, other):
        if isinstance(other, numInterval):
            if self._symbol in ["<=", "<"] and other._symbol in [">=", ">"]:
                return False
            if self._symbol in [">=", ">", ''] and other._symbol in ["<=", "<", '']:
                return super(numInterval, self).__ge__(other)
            if self._symbol == "<":
                return super(numInterval, self).__gt__(other)
        if self._symbol == "<":
            return super(numInterval, self).__gt__(other)
        else:
            return super(numInterval, self).__ge__(other)

    def __lt__(self, other):
        if isinstance(other, numInterval):
            if self._symbol in [">=", ">"] and other._symbol in ["<=", "<"]:
                return False

        return not self.__ge__(other)

    def __le__(self, other):
        if isinstance(other, numInterval):
            if self._symbol in [">=", ">"] and other._symbol in ["<=", "<"]:
                return False
            if self._symbol in ["<=", "<", ''] and other._symbol in [">=", ">", '']:
                return super(numInterval, self).__le__(other)
            if self._symbol == ">":
                return super(numInterval, self).__lt__(other)

        return super(numInterval, self).__le__(other)

    def __str__(self):
        if self._symbol:
            return "{}{}".format(self._symbol, str(self._n))
        else:
            return super(numInterval, self).__str__()

    def __repr__(self):
        if self._symbol:
            return "{} {}".format(self._symbol, str(self._n))
        else:
            return super(numInterval, self).__repr__()
