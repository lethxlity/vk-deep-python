import unittest
from unittest import mock
from first_task import SomeModel
from first_task import predict_message_mood


class TestModel(unittest.TestCase):
    def setUp(self):
        self.model = SomeModel()

    def test_predictions(self):
        predictions = {0: "неуд", 0.2: "неуд", 0.5: "норм", 0.9: "отл",
                       1: "отл", 0.3: "норм", 0.8: "норм"}
        with mock.patch("test_first_task.SomeModel.predict") as mock_prediction:
            for key, value in predictions.items():
                mock_prediction.return_value = key
                self.assertEqual(predict_message_mood("Строка", self.model), value)
