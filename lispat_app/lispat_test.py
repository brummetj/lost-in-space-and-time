from unittest import TestCase
from controller.app import run

class TestConsole(TestCase):
    def test_basic(self):
        run()
