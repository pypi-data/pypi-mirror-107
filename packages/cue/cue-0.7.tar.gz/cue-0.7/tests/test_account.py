from tests.unit_test import UnitTest


class TestAcc(UnitTest):

    def test_acc_1(self):
        """init loads account data"""
        from cue.account import Account
        a = Account('110_cash.acc')
        assert 'dr' in a

    def test_acc_2(self):
        """enter called directly raises error"""
        from cue.account import Account
        a = Account('110_cash.acc')
        try:
            a.enter('DR', 'test_acc_2', '1.23')
        except Exception as e:
            assert 'invalid caller' in str(e)
        else:
            raise RuntimeError('no exception was raised')

    def test_acc_3(self):
        """auto creates account file"""
        from cue.account import Account
        a = Account.create('111 - Test', 'DR')
        with a.path.open() as f:
            assert 'bal:' in f.read()
