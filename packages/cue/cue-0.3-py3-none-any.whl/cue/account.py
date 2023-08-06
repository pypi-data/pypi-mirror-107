# cue
# Accounting system for Linux
# Copyright (c) 2021 Kosciuszko Cloud
# Open source, MIT license: http://www.opensource.org/licenses/mit-license.php
"""
Account

"""
import inspect
from pathlib import Path

from cue.data import Data
from cue.arithmetic import Decimal


class Account(Data):
    """a ledger account"""

    def __init__(self, filename, data=None):
        path = Path(filename)
        super().__init__(path, data)

    def enter(self, entry_type, label, amt):
        """post an entry"""
        caller = inspect.stack()[1].function
        valid_callers = ['post']
        if caller not in valid_callers:
            raise Exception(f'invalid caller: {caller}')
        typ = entry_type.lower()
        self[typ].append([label, amt.quantize()])
        self._balance()
        self.dump()

    def _balance(self):
        """calculate the account balance"""
        total = (sum(dr[-1] for dr in self['dr']) -
                 sum(cr[-1] for cr in self['cr']))
        if self['bal_type'] == 'CR':
            total = -1 * total
        self['bal'] = Decimal(total).quantize()
