import unittest
from custom_list import CustomList


class TestCustomList(unittest.TestCase):
    def assertEquality(self, obj1, obj2):
        # Check equality of two same length non-empty lists
        for i in range(len(obj1)):
            self.assertAlmostEqual(obj1[i], obj2[i], None, 1e-9)

    def test_list_behaviour(self):

        custom_list = CustomList([1, 2, 3, 4.2])
        custom_list.append(-5)
        self.assertEquality(custom_list, [1, 2, 3, 4.2, -5])
        self.assertEquality(custom_list, CustomList([1, 2, 3, 4.2, -5]))

        copy = custom_list.copy()
        self.assertEquality(copy, [1, 2, 3, 4.2, -5])
        self.assertEquality(copy, CustomList([1, 2, 3, 4.2, -5]))

        self.assertIsInstance(copy, CustomList)

        custom_list.extend([6, 7])
        self.assertEquality(custom_list, [1, 2, 3, 4.2, -5, 6, 7])
        self.assertEquality(custom_list, CustomList([1, 2, 3, 4.2, -5, 6, 7]))

        custom_list.insert(0, 0)
        self.assertEquality(custom_list, [0, 1, 2, 3, 4.2, -5, 6, 7])
        self.assertEquality(custom_list, CustomList([0, 1, 2, 3, 4.2, -5, 6, 7]))

        custom_list.pop(2)

        self.assertEquality(custom_list, [0, 1, 3, 4.2, -5, 6, 7])
        self.assertEquality(custom_list, CustomList([0, 1, 3, 4.2, -5, 6, 7]))

        self.assertEqual(custom_list.count(1), 1)

        self.assertEqual(custom_list.index(3), 2)

        custom_list.remove(-5)
        self.assertEquality(custom_list, [0, 1, 3, 4.2, 6, 7])
        self.assertEquality(custom_list, CustomList([0, 1, 3, 4.2, 6, 7]))

        custom_list.reverse()
        self.assertEquality(custom_list, [7, 6, 4.2, 3, 1, 0])
        self.assertEquality(custom_list, CustomList([7, 6, 4.2, 3, 1, 0]))

        custom_list.sort()
        self.assertEquality(custom_list, [0, 1, 3, 4.2, 6, 7])
        self.assertEquality(custom_list, CustomList([0, 1, 3, 4.2, 6, 7]))

        self.assertIsInstance(custom_list, CustomList)

        custom_list.clear()
        self.assertEqual(len(custom_list), 0)

    def test_custom_list_behaviour(self):

        self.assertEquality(CustomList([1, 2]) + CustomList([3, 2, 0]), CustomList([4, 4, 0]))
        self.assertEquality(CustomList([1.3, 2.8]) + CustomList([3, 2, 0]), CustomList([4.3, 4.8, 0]))
        self.assertEquality(CustomList([]) + CustomList([3, 2, 0]), CustomList([3, 2, 0]))
        self.assertEquality(CustomList([]) + CustomList([]), CustomList([]))

        self.assertEquality(CustomList([1, 2]) + [3, 2, 0], CustomList([4, 4, 0]))
        self.assertEquality(CustomList([1.3, 2.8]) + [3, 2, 0], CustomList([4.3, 4.8, 0]))
        self.assertEquality(CustomList([]) + [3, 2, 0], CustomList([3, 2, 0]))
        self.assertEquality(CustomList([]) + [], CustomList([]))

        self.assertEquality(CustomList([1, 2]) - CustomList([3, 2, 2]), CustomList([-2, 0, -2]))
        self.assertEquality(CustomList([1.3, 2.8]) - CustomList([3, 3, 2]), CustomList([-1.7, -0.2, -2]))
        self.assertEquality(CustomList([]) - CustomList([3, 2, 0]), CustomList([-3, -2, 0]))
        self.assertEquality(CustomList([]) - CustomList([]), CustomList([]))

        self.assertTrue(CustomList([1, 2, 3]) > CustomList([1, 2, 1, 0]))
        self.assertTrue(CustomList([1, 2, 3]) >= CustomList([1, 2, 1, 0]))
        self.assertTrue(CustomList([1, 2, 3]) >= CustomList([1, 2, 1, 2]))
        self.assertTrue(CustomList([1, 2, 0, 0, 0]) < CustomList([1, 2, 5]))
        self.assertTrue(CustomList([1, 2, 0, 0, 0]) <= CustomList([1, 2, 5]))
        self.assertTrue(CustomList([1, 2, 0, 5, 0]) <= CustomList([1, 2, 5]))
        self.assertTrue(CustomList([1, 2, 0, 6, -1]) == CustomList([1, 2, 5]))
        self.assertTrue(CustomList([1, 2]) != CustomList([1, 2, 5]))
