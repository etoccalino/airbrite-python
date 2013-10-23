import unittest
import airbrite.api
import airbrite.client


class AirbriteTestCase (unittest.TestCase):

    def setUp(self):
        self.c = airbrite.client.Client()
