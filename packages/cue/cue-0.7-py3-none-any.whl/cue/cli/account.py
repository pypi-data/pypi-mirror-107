# cue
# Accounting system for Linux
# Copyright (c) 2021 Kosciuszko Cloud
# Open source, MIT license: http://www.opensource.org/licenses/mit-license.php
"""
Account CLI

"""
import cue.account


class Account(cue.account.Account):
    """account CLI tools"""

    @classmethod
    def auto(cls, title, bal_type):
        """create an account"""
        filename = f'{sanitize_(title)}.acc'
        data = {
            'bal_type': bal_type,
            'dr': [],
            'cr': [],
            'closed': False
        }
        a = cls(filename, data)
        a.write()
        return a

    def write(self):
        """write the account file"""
        self._balance()
        self.dump()


def sanitize_(acc_name):
    """convert account names to filenames"""
    return (acc_name.replace(' - ', '_')
                    .replace(' ', '_')
                    .lower())
