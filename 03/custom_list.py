import copy


class CustomList(list):
    def __add__(self, other):
        if self.__len__() < other.__len__():
            left = [self[i] + other[i] for i in range(self.__len__())]
            left.extend(other[self.__len__():])
        else:
            left = [self[i] + other[i] for i in range(other.__len__())]
            left.extend(self[other.__len__():])
        return CustomList(left)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if self.__len__() < other.__len__():
            left = [self[i] - other[i] for i in range(self.__len__())]
            left.extend([-other[i] for i in range(self.__len__(), other.__len__())])
        else:
            left = [self[i] - other[i] for i in range(other.__len__())]
            left.extend([self[i] for i in range(other.__len__(), self.__len__())])
        return CustomList(left)

    def __rsub__(self, other):
        temp = CustomList(other)
        return temp.__sub__(self)

    def sum(self):
        res = 0
        for i in range(self.__len__()):
            res += self[i]
        return res

    def __lt__(self, other):
        return self.sum() < other.sum()

    def __le__(self, other):
        return self.sum() <= other.sum()

    def __eq__(self, other):
        return self.sum() == other.sum()

    def __ne__(self, other):
        return self.sum() != other.sum()

    def __gt__(self, other):
        return self.sum() > other.sum()

    def __ge__(self, other):
        return self.sum() >= other.sum()

    def copy(self):
        return copy.copy(self)

