class MyDescriptor():

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        instance.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        self.name = name


class Integer(MyDescriptor):
    def __set__(self, instance, value):
        if isinstance(value, int) or value is None:
            instance.__dict__[self.name] = value
        else:
            raise TypeError


class String(MyDescriptor):
    def __set__(self, instance, value):
        if isinstance(value, str) or value is None:
            instance.__dict__[self.name] = value
        else:
            raise TypeError


class PositiveInteger(MyDescriptor):
    def __set__(self, instance, value):
        if value is None:
            instance.__dict__[self.name] = value
        elif isinstance(value, int):
            if value >= 0:
                instance.__dict__[self.name] = value
            else:
                raise ValueError
        else:
            raise TypeError


class Data():
    num = Integer()
    name = String()
    price = PositiveInteger()

    def __init__(self, num=None, name=None, price=None):
        self.num = num
        self.name = name
        self.price = price
