import unittest
from metaclass import CustomClass


class TestCustomClass(unittest.TestCase):
    def setUp(self):
        self.instance = CustomClass()

    def test_class(self):
        self.assertEqual(CustomClass.custom_x, 50)
        with self.assertRaises(AttributeError):
            temp = CustomClass.x

    def test_instance(self):
        self.instance.y = 1
        self.assertEqual(self.instance.custom_y, 1)
        with self.assertRaises(AttributeError):
            temp = self.instance.y

        self.instance.custom_val = 99
        self.assertEqual(self.instance.custom_val, 99)
        with self.assertRaises(AttributeError):
            temp = self.instance.val

        self.assertEqual(self.instance.custom_line(), 100)
        with self.assertRaises(AttributeError):
            temp = self.instance.line()

        self.assertEqual(str(self.instance), "Custom_by_metaclass")
