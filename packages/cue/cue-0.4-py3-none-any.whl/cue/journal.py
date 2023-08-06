# cue
# Accounting system for Linux
# Copyright (c) 2021 Kosciuszko Cloud
# Open source, MIT license: http://www.opensource.org/licenses/mit-license.php
"""
Journal

"""
from datetime import datetime
from pathlib import Path

from cue.data import Data
from cue.account import Account
from cue.arithmetic import journal_sum


class Journal(Data):
    """a journal"""

    def __init__(self, filename=None, data=None):
        if filename:
            path = Path(filename)
        else:
            ts = f'{datetime.now():%Y%m%d%H%M%S}'
            filename = f'{ts}-operator.jnl'
            path = Path('.cue') / 'current' / filename
        super().__init__(path, data)

    def post(self):
        """post items to the T-accounts"""
        if not self._balanced():
            raise AssertionError('journal does not balance')

        # assign a sequential number
        self['id'] = self.get_next()

        # move to .cue/posted
        path = self.path
        new_parent = self.ledger.path / '.cue' / 'posted'
        self.path = path.rename(new_parent / path.name)
        self.protect()

        # post the entries
        for item_type, account, label, amt in self['items']:
            a = Account(account)
            a.enter(item_type, label, amt)

    def _balanced(self):
        """journal is balanced"""
        p = self.ledger['precision']
        return journal_sum(self['items']) == 0
