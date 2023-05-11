import sys
import unittest
import warnings
from unittest import mock
from fetcher import AsyncFetcher
from aioresponses import aioresponses


class TestFetcher(unittest.TestCase):
    def test_fetcher_calls(self):
        if not sys.warnoptions:
            warnings.simplefilter("ignore")
        with mock.patch("sys.argv", ["", "10", "urls_1.txt"]):
            with aioresponses() as response_mock:
                body1 = open("bodies/body_1.txt", "r", encoding="utf8")
                body2 = open("bodies/body_2.txt", "r", encoding="utf8")
                body3 = open("bodies/body_3.txt", "r", encoding="utf8")
                body4 = open("bodies/body_4.txt", "r", encoding="utf8")
                body5 = open("bodies/body_5.txt", "r", encoding="utf8")
                response_mock.get('https://stackoverflow.com/questions/10810249/python-socket-multiple-clients', body=body1.read())
                response_mock.get('https://en.wikipedia.org/wiki/Marcus_Aurelius', body=body2.read())
                response_mock.get('https://sliding.toys/mystic-square/8-puzzle/', body=body3.read())
                response_mock.get('https://paint.toys/', body=body4.read())
                response_mock.get('https://poedb.tw/us/', body=body5.read())
                test_fetcher = AsyncFetcher(int(sys.argv[1]), open(sys.argv[2], "r", encoding="utf8"))
                with mock.patch('builtins.print') as mocked_print:
                    test_fetcher.start()
                    mocked_print.assert_has_calls([mock.call("https://stackoverflow.com/questions/10810249/python-socket-multiple-clients{'to': 79, 'this': 74, 'a': 70, 'the': 66, 'socket': 51, 'answer': 50, '=': 49}"),
                                                   mock.call("https://en.wikipedia.org/wiki/Marcus_Aurelius{'the': 961, 'of': 599, 'marcus': 528, 'and': 447, '^': 372, 'in': 345, 'to': 330}"),
                                                   mock.call("https://sliding.toys/mystic-square/8-puzzle/{'the': 5, 'to': 4, 'a': 4, 'toys': 3, '8': 3, 'sliding': 2, 'puzzle': 2}"),
                                                   mock.call("https://poedb.tw/us/{'the': 41, 'of': 24, 'damage': 18, 'vaal': 15, 'atlas': 13, 'eldritch': 13, 'crucible': 10}"),
                                                   mock.call("https://paint.toys/{'a': 7, 'your': 6, 'the': 6, 'to': 5, 'with': 5, 'paint': 4, 'of': 4}")], any_order=True)

    def test_fetcher_call_count(self):
        if not sys.warnoptions:
            warnings.simplefilter("ignore")
        with mock.patch("sys.argv", ["", "10", "urls_2.txt"]):
            with aioresponses() as response_mock:
                for i in range(100):
                    response_mock.get('https://en.wikipedia.org/wiki/Marcus_Aurelius', body="TEST TEST TEST")
                test_fetcher = AsyncFetcher(int(sys.argv[1]), open(sys.argv[2], "r", encoding="utf8"))
                with mock.patch('builtins.print') as mocked_print:
                    test_fetcher.start()
                    assert mocked_print.call_count == 100
