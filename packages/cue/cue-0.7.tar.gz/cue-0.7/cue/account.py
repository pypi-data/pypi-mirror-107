# cue
# Accounting system for Linux
# Copyright (c) 2021 Kosciuszko Cloud
# Open source, MIT license: http://www.opensource.org/licenses/mit-license.php
"""
Account

"""
import inspect
from pathlib import Path
from itertools import zip_longest
from functools import reduce

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
        self.dump()

    def _balance(self):
        """calculate the account balance"""
        total = (sum(dr[-1] for dr in self['dr']) -
                 sum(cr[-1] for cr in self['cr']))
        if self['bal_type'] == 'CR':
            total = -1 * total
        self['bal'] = Decimal(total).quantize()

    @classmethod
    def create(cls, title, bal_type):
        """create an account"""
        filename = f'{sanitize_(title)}.acc'
        data = {
            'bal_type': bal_type,
            'dr': [],
            'cr': [],
            'closed': False
        }
        a = cls(filename, data)
        a.dump()
        return a

    def dump(self):
        """update balance and dump"""
        self._balance()
        super().dump()

    def __str__(self):
        """format as T-account"""
        bal_label = ('Closing balance' if
                     self['closed'] else
                     'Balance')
        default = [[bal_label, self['bal']]]
        entries = self['dr'] + self['cr'] + default * 2
        wdesc = reduce(lambda x, y: max(x, len(y[0])),
                       entries, 0)
        wamt = reduce(lambda x, y: max(x, len(str(y[1]))),
                      entries, 0)
        title = (self.path.stem
                 .replace('_', ' - ', 1)
                 .replace('_', ' ').title())
        wbox = 5
        wtot = max(39, len(title) + 2, (wdesc + wamt) * 2 + wbox)
        if not wtot % 2:
            wtot += 1
        wdesc = wtot // 2 - (wamt + 2)
        wbal = wdesc + wamt + 1
        bal_pos = wbal if self['bal_type'] == 'DR' else wtot
        lines = ['', f'{title: ^{wtot}}', f"{'╤':═^{wtot}}"]
        data = zip_longest(self['dr'], self['cr'], fillvalue=['', ''])
        for d in data:
            lines.append(f'{d[0][0]: <{wdesc}} {d[0][1]: >{wamt}} │ ' +
                         f'{d[1][0]: <{wdesc}} {d[1][1]: >{wamt}}')
        rule = f"{'':─>{wbal}}"
        bal = f"{bal_label: <{wdesc}} {self['bal']: >{wamt}}"
        lines += ['', f"{rule: >{bal_pos}}", f'{bal: >{bal_pos}}', '']
        return '\n'.join(lines)


def sanitize_(acc_name):
    """convert account names to filenames"""
    return (acc_name.replace(' - ', '_')
                    .replace(' ', '_')
                    .lower())
