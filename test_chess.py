import re

from chess_main import *

class TestNotationRE(unittest.TestCase):
    x = 5
    valid_moves = ['e4',
        'Nf3',
        'qh5',
        'exd5',
        'nxd5',
        'ndxe6',
        'bxe6',
        'Bb5',
        'e6',
        'h6',
        'a2',
        'cxd4',
        'gh2',
        'Q5h1',
        'nfg1',
        'rb5xh5',
        'c5']

    invalid_moves = [
        'jh5',
        'bxa12',
        'kjhc6',
        'nkk6',
        'h50',
        'zd1'
    ]

    def test_valid(self):
        for test in TestNotationRE.valid_moves:
            match = re.search(pattern, test, re.IGNORECASE)
            self.assertTrue(match)


    def test_invalid(self):
        for test in TestNotationRE.invalid_moves:
            match = re.search(pattern, test, re.IGNORECASE)
            self.assertFalse(match)
