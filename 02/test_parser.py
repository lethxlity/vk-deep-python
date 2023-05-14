import unittest
from unittest import mock
from unittest.mock import call
from parser import parse_json


class TestParser(unittest.TestCase):

    def test_callback_args(self):
        str_json = '{"age":"42"}'
        mock_callback = mock.MagicMock()
        parse_json(str_json, ["age"], ["42"], mock_callback)
        self.assertEqual(mock_callback.call_args,
                         call(('age', '42')))
        self.assertEqual(mock_callback.call_count, 1)

        str_json = '{"age":"42 44 55","name":"Chris Anna John"}'
        mock_callback = mock.MagicMock()
        parse_json(str_json, ["age"], ["42", "Anna"], mock_callback)
        self.assertEqual(mock_callback.call_args,
                         call(('age', '42')))
        self.assertEqual(mock_callback.call_count, 1)

        str_json = '{"age":"42 44 55","name":"Chris Anna John"}'
        mock_callback = mock.MagicMock()
        parse_json(str_json, ["age", "name"], ["42", "Anna"], mock_callback)
        self.assertEqual(mock_callback.call_args_list,
                         [call(("age", "42")),
                          call(("name", "Anna"))])
        self.assertEqual(mock_callback.call_count, 2)

        str_json = '{"age":"42", "name1":"Chris Anna John","name2":"Chris Anna John"}'
        mock_callback = mock.MagicMock()
        parse_json(str_json, ["name1", "name2"], ["Chris", "Anna", "42"], mock_callback)
        self.assertEqual(mock_callback.call_args_list,
                         [call(("name1", "Chris")),
                          call(("name1", "Anna")),
                          call(("name2", "Chris")),
                          call(("name2", "Anna"))])
        self.assertEqual(mock_callback.call_count, 4)

    def test_callback_similar_keywords(self):
        str_json = '{"names":"Johnathan Johnson Johns St.John"}'
        mock_callback = mock.MagicMock()
        self.assertIsNone(parse_json(str_json, ["names"], ["John"], mock_callback))
        self.assertEqual(mock_callback.call_count, 0)

        str_json = '{"names":"Johnathan John"}'
        mock_callback = mock.MagicMock()
        parse_json(str_json, ["names"], ["John"], mock_callback)
        self.assertEqual(mock_callback.call_args,
                         call(('names', 'John')))
        self.assertEqual(mock_callback.call_count, 1)

    def test_callback_repetitions(self):
        str_json = '{"names":"John Chris John"}'
        mock_callback = mock.MagicMock()
        parse_json(str_json, ["names"], ["John"], mock_callback)
        self.assertEqual(mock_callback.call_count, 2)

    def test_none_args(self):
        mock_callback = mock.MagicMock()
        str_json = '{"age":"42"}'
        with self.assertRaises(TypeError):
            parse_json(json_str=str_json,
                       required_fields=["age"],
                       keywords=["42"])
        with self.assertRaises(TypeError):
            parse_json(required_fields=["age"],
                       keywords=["42"],
                       keyword_callback=mock_callback)
        with self.assertRaises(TypeError):
            parse_json(json_str=str_json,
                       keywords=["42"],
                       keyword_callback=mock_callback)
        with self.assertRaises(TypeError):
            parse_json(json_str=str_json,
                       required_fields=["age"],
                       keyword_callback=mock_callback)
