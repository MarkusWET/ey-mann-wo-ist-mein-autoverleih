import unittest
import app


class SetupTest(unittest.TestCase):
    def setUp(self):
        test_app = app.create_app({"TESTING": True})
        assert True

    def test(self):
        assert True

    def test2(self):
        assert True

    def test3(self):
        assert True

    def test4(self):
        assert True
