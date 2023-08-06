import subprocess, os
from pathlib import Path

from cue.ledger import Ledger
from tests.unit_test import UnitTest


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

    def test_lgr_3(self):
        """boilerplate creates temporary settings file"""
        from cue.ledger import Ledger
        Ledger.boilerplate()
        filename = 'temp__Ledger__settings.yml'
        assert filename in os.listdir()

    def test_lgr_4(self):
        """boilerplate/wizard raise exception for existing ledger"""
        from cue.ledger import Ledger
        try:
            Ledger.boilerplate()
        except Exception as e:
            assert 'Existing ledger' in str(e)
        else:
            raise RuntimeError('no exception was raised')

    def test_lgr_5(self):
        """wizard creates temporary settings file for custom COA"""
        assert True # this doesn't exist yet

    def test_lgr_6(self):
        """wizard creates permanent settings file for default COA"""
        assert True # this doesn't exist yet
