import subprocess, os
from pathlib import Path

from tests.unit_test import UnitTest


class TestCli(UnitTest):

    def test_cli_bin_1(self):
        """cue parses command line args"""
        sp = subprocess.run(['cue', 'echo', 'test', 'bin'],
                            capture_output=True)
        assert sp.stdout.decode('utf-8').strip() == 'test bin'

    def test_cli_acc_1(self):
        """auto creates account file"""
        from cue.cli.account import Account
        a = Account.auto('111 - Test', 'DR')
        with a.path.open() as f:
            assert 'bal:' in f.read()

    def test_cli_inv_1(self):
        """parse parses a text invoice correctly"""
        from cue.cli.invoice import Invoice
        filename = 'temp__Invoice__hollywood_muscle.txt'
        inv = Invoice.parse(Path(filename))
        assert 'total' in inv

    def test_cli_inv_2(self):
        """issue assigns sequential number"""
        from cue.cli.invoice import Invoice
        filename = 'temp__Invoice__hollywood_muscle.txt'
        inv = Invoice.parse(Path(filename))
        inv.issue()
        assert inv['number'] == 564

    def test_cli_inv_3(self):
        """issue cleans up temp file"""
        from cue.cli.invoice import Invoice
        filename = 'temp__Invoice__hollywood_muscle.txt'
        path = Path(filename)
        inv = Invoice.parse(path)
        inv.issue()
        try:
            path.read_text()
        except:
            assert True
        else:
            raise RuntimeError('tempfile was not cleaned up')

    def test_cli_lgr_1(self):
        """boilerplate creates temporary settings file"""
        from cue.cli.ledger import Ledger
        Ledger.boilerplate()
        filename = 'temp__Ledger__settings.yml'
        assert filename in os.listdir()

    def test_cli_lgr_2(self):
        """wizard creates temporary settings file for custom COA"""
        assert True # this doesn't exist yet

    def test_cli_lgr_3(self):
        """wizard creates permanent settings file for default COA"""
        assert True # this doesn't exist yet

    def test_cli_lgr_4(self):
        """commit creates permanent settings file"""
        from cue.cli.ledger import Ledger
        lgr = Ledger.commit()
        assert 'precision' in lgr

    def test_cli_lgr_5(self):
        """boilerplate/wizard raise exception for existing ledger"""
        from cue.cli.ledger import Ledger
        try:
            Ledger.boilerplate()
        except Exception as e:
            assert 'Existing ledger' in str(e)
        else:
            raise RuntimeError('no exception was raised')
