import unittest
from generator import gen


class TestGenerator(unittest.TestCase):
    def test_normal(self):
        for found_string in gen("second_task_testcases/testcase_1.txt", ["лекарство"]):
            self.assertEqual(found_string, "Рукава как лекарство для вен\n")
        for found_string in gen("second_task_testcases/testcase_1.txt", ["год"]):
            self.assertEqual(found_string, "Я прожил целый год без тебя\n")
        for found_string in gen("second_task_testcases/testcase_1.txt", ["вкус"]):
            self.assertEqual(found_string, "Полюбил вкус твоих сигарет\n")

    def test_repeating_strings(self):
        for found_string in gen("second_task_testcases/testcase_2.txt", ["ты"]):
            self.assertEqual(found_string, "Ты не пройдёшь!\n")

    def test_empty_txt(self):
        for found_string in gen("second_task_testcases/testcase_3.txt", ["ты"]):
            self.assertEqual(found_string, None)

    def test_empty_list(self):
        for found_string in gen("second_task_testcases/testcase_2.txt", []):
            self.assertEqual(found_string, None)

    def test_similar_words(self):
        for found_string in gen("second_task_testcases/testcase_4.txt", ["человек"]):
            self.assertEqual(found_string, "Человек человеку волк\n")

    def test_repeating_words(self):
        for found_string in gen("second_task_testcases/testcase_5.txt", ["Алексей"]):
            self.assertEqual(found_string, "Алексей о Алексей\n")

    def test_similar_words_another(self):
        for found_string in gen("second_task_testcases/testcase_6.txt", ["кактус"]):
            self.assertEqual(found_string, None)

    def test_similar_multiple_filters(self):
        output = []
        for found_string in gen("second_task_testcases/testcase_4.txt", ["человек", "волк"]):
            output.append(found_string)
        self.assertEqual(output, ["Человек человеку волк\n"])
