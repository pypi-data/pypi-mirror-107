import os
from collections import OrderedDict

from tests.unit_test import UnitTest


class TestJnl(UnitTest):

    def test_jnl_1(self):
        """init loads journal data"""
        from cue.journal import Journal
        j = Journal('2021-04-13_operator.jnl')
        assert 'items' in j

    def test_jnl_2(self):
        """post journal raises error if unbalanced"""
        from cue.journal import Journal
        j = Journal('2021-04-13_operator.jnl')
        try:
            j.post()
        except Exception as e:
            assert 'does not balance' in str(e)
        else:
            raise RuntimeError('no exception was raised')

    def test_jnl_3(self):
        """journal instantiates itself in .cue/current"""
        from cue.journal import Journal
        items = ['item']
        j = Journal(data=OrderedDict(items=items,
                                     posted=False))
        assert len(os.listdir('.cue/current')) > 0

    def test_jnl_4(self):
        """post journal attaches an integer identifier"""
        from cue.journal import Journal
        j = Journal('20210421082500-operator.jnl')
        j.post()
        assert type(j['id']) is int

    def test_jnl_5(self):
        """post journal removes write permissions from file"""
        from cue.journal import Journal
        j = Journal('20210421082500-operator.jnl')
        j.post()
        try:
            j.path.write_text('something')
        except Exception as e:
            assert 'Permission denied' in str(e)
        else:
            raise RuntimeError('no exception was raised')
