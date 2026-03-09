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

    def test_try_valid_attribute(self):
        '''
        @private
        Tests that a valid command returns true
        through the trying_attribute function
        '''
        assert ui.trying_attribute(print("HI")) is True

    def test_check_ow_and_lastfm_no_keyword(self):
        '''
        @private
        Tests that checking the transpose function
        works on a string that doesn't contain a keyword.
        '''
        assert ui.check_ow_and_lastfm("Hi there") == "Hi there"

    def test_invalid_port(self):
        '''
        @private
        Tests that an invalid port/server will return False.
        '''
        assert ds_client.send(
            "clotho.ics.uci.edu",
            1234,
            "joseph",
            "there",
            "Hi"
            ) is False
    
    def test_valid_send(self):
        '''
        @private
        Tests that valid information will return True.
        '''
        assert ds_client.send(
            "clotho.ics.uci.edu",
            2021,
            "joseph",
            "there",
            "Hi"
            ) is True
