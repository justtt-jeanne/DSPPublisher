# JEANNE NGUYEN
# jeannen2@uci.edu
# 57923737
# pylint: disable=invalid-name, protected-access
'''
Testing all (probably closer to 70%) of all the code across
all the different modules dealing with try and checking things.
'''

from pathlib import Path
import unittest
import a4
import ui
import ds_client


class Test_TestingTryingChecking(unittest.TestCase):
    '''
    Testing class that tests any function that checks things
    '''
    def test_check_path(self):
        '''
        @private
        Tests that an invalid path will return path.
        Does not test a valid path because I cannot
        guarantee what path is on the person's computer.
        '''
        assert a4.check_path(Path("abcdef")) is False

    def test_try_invalid_profile(self):

        assert ui.trying_attribute(print("HI")) is True

    def test_check_ow_and_lastfm_(self):
        assert ui.check_ow_and_lastfm("Hi there") == "Hi there"

    def test_invalid_port(self):
        assert ds_client.send(
            "clotho.ics.uci.edu",
            1234,
            "joseph",
            "there",
            "Hi"
            ) is False
    
    def test_valid_send(self):
        assert ds_client.send(
            "clotho.ics.uci.edu",
            2021,
            "joseph",
            "there",
            "Hi"
            ) is True
