import unittest
from descriptor import Data


class TestDescriptor(unittest.TestCase):
    def setUp(self):
        self.data = Data()

    def test_exceptions(self):
        with self.assertRaises(TypeError):
            self.data.num = 1.2
        with self.assertRaises(TypeError):
            self.data.name = 1
        with self.assertRaises(TypeError):
            self.data.price = 1.2
        with self.assertRaises(ValueError):
            self.data.price = -1

    def test_normal_behaviour(self):
        self.data.num = 1
        self.assertEqual(self.data.num, 1)
        self.data.name = "name"
        self.assertEqual(self.data.name, "name")
        self.data.price = 10
        self.assertEqual(self.data.price, 10)
        self.data.price = 0
        self.assertEqual(self.data.price, 0)
