import json
import unittest
import ujson

from cjson import cutils


class TestParser(unittest.TestCase):

    def test_equality(self):
        with open('data2.txt', 'r') as file:
            data = file.read().replace('\n', ' ')
            self.assertEqual(cutils.loads(data), json.loads(data))
            self.assertEqual(cutils.loads(data), ujson.loads(data))
