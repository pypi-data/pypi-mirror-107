import os

from tests.unit_test import UnitTest
from cue.ledger import Ledger


class TestLgr(UnitTest):


    def test_lgr_1(self):
        """init loads settings for existing ledger"""
        org = Ledger()
        assert 'precision' in org

    def test_lgr_2(self):
        """clean removes cue dir and T-accounts"""
        Ledger.clean()
        ls = os.listdir()
        assert '.cue' not in ls
        assert not [f for f in ls if f.endswith('.acc')]
