class CustomMeta(type):

    def __new__(mcs, name, bases, classdict):
        cls = super().__new__(mcs, name, bases, classdict)
        return cls

    def __init__(cls, name, bases, classdict):
        super().__init__(name, bases, classdict)

    def __call__(cls, *args, **kwargs):
        return super().__call__(*args, **kwargs)

    def __setattr__(cls, name, val):
        if name != "_corrected":
            if not name.startswith("custom_"):
                name = "custom_"+name
        if name in cls.__dict__:
            cls.name = val
        else:
            return super().__setattr__(name, val)

    def __getattribute__(cls, item):
        corrected = False
        try:
            corrected = super().__getattribute__("_corrected")
        except AttributeError:
            super().__setattr__("_corrected", False)
            corrected = False
        finally:
            if not corrected:
                super().__setattr__("_corrected", True)
                to_be_deleted = {}
                for attr, value in cls.__dict__.items():
                    if attr != "_corrected":
                        if not attr.startswith("__") and not attr.endswith("__") and not attr.startswith("custom_"):
                            to_be_deleted[attr] = value
                for attr, value in to_be_deleted.items():
                    super().__delattr__(attr)
                    super().__setattr__("custom_" + attr, value)
        return super().__getattribute__(item)


class CustomClass(metaclass=CustomMeta):
    x = 50

    def __init__(self, val=99):
        self.val = val

    def __setattr__(cls, name, val):
        if name != "_corrected":
            if not name.startswith("custom_"):
                name = "custom_" + name
        if name in cls.__dict__:
            cls.name = val
        else:
            return super().__setattr__(name, val)

    def __getattribute__(cls, item):
        corrected = False
        try:
            corrected = super().__getattribute__("_corrected")
        except AttributeError:
            super().__setattr__("_corrected", False)
            corrected = False
        finally:
            if not corrected:
                super().__setattr__("_corrected", True)
                to_be_deleted = {}
                for attr, value in cls.__dict__.items():
                    if attr != "_corrected":
                        if not attr.startswith("__") and not attr.endswith("__") and not attr.startswith("custom_"):
                            to_be_deleted[attr] = value
                for attr, value in to_be_deleted.items():
                    super().__delattr__(attr)
                    super().__setattr__("custom_" + attr, value)
        return super().__getattribute__(item)

    def line(self):
        return 100

    def __str__(self):
        return "Custom_by_metaclass"
