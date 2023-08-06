# cue
# Accounting system for Linux
# Copyright (c) 2021 Kosciuszko Cloud
# Open source, MIT license: http://www.opensource.org/licenses/mit-license.php
"""
Parent class for data artifacts

"""
import re
from pathlib import Path
from collections import OrderedDict

from ruamel.yaml import YAML

from cue.arithmetic import Decimal
from cue.ledger import Ledger

read_only = 0o444


class Data(OrderedDict):
    """a data artifact"""

    def __init__(self, path=None, data=dict()):
        self.ledger = Ledger()
        if data:
            self.path = self.ledger.path / path
        elif path:
            self.path = path
            data = yaml.load(self.path)
        super().__init__(**data)

    def __getitem__(self, key):
        try:
            item = super().__getitem__(key)
        except KeyError:
            item = Decimal().quantize()
        return item

    def get_next(self):
        """next integer in the subclass's sequence"""
        cls = self.__class__.__name__.lower()
        self.ledger[f'{cls}_seq'] += 1
        self.ledger.dump()
        return self.ledger[f'{cls}_seq']

    def dump(self):
        """save to file in !!omap form"""
        yaml.dump(OrderedDict(self), self.path)

    def protect(self):
        """make a data artifact file read only"""
        self.path.chmod(read_only)


yaml = YAML()
yaml.register_class(Decimal)
