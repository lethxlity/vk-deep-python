import unittest
from unittest import mock
from second_hw import parse_json


class TestParser(unittest.TestCase):
    def test_callback_count(self):
        str_json = '{"age":"42"}'
        mock_callback = mock.MagicMock()
        mock_callback.call_count = 0
        parse_json(str_json, ["age"], ["42"], mock_callback)
        self.assertEqual(mock_callback.call_count, 1)
        mock_callback.call_count = 0
        parse_json(str_json, ["age"], ["43"], mock_callback)
        self.assertEqual(mock_callback.call_count, 0)
        mock_callback.call_count = 0
        parse_json(str_json, ["Age"], ["42"], mock_callback)
        self.assertEqual(mock_callback.call_count, 0)

    def test_empty_args(self):
        mock_callback = mock.MagicMock()
        str_json = '{"age":"42"}'
        self.assertIsNone(parse_json(str_json, [], ["42"], mock_callback))
        self.assertIsNone(parse_json(str_json, ["age"], [], mock_callback))
        self.assertIsNone(parse_json(str_json, [], [], mock_callback))
