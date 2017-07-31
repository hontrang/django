"""
declare simple testcase, only http test still now
"""
import json
import time
import unittest
import logging
import bson
from random import randint, randrange

from rest_framework.test import APIClient
logger = logging.getLogger(__name__)


# Create your tests here.


class MongoEngineTestCase(unittest.TestCase):
    """
    Testcases to validate http service usage, use rest framework api test
    """

    def setUp(self):
        """
        Setting up testcases
        """

    def tearDown(self):
        """
        Cleanup testcases when complete
        """
