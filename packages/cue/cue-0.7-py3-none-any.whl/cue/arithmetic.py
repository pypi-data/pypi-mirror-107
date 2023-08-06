# cue
# Accounting system for Linux
# Copyright (c) 2021 Kosciuszko Cloud
# Open source, MIT license: http://www.opensource.org/licenses/mit-license.php
"""
Decimal stuff

"""
import decimal

from cue.ledger import Ledger

rounding_strategy = decimal.ROUND_HALF_UP


class Decimal(decimal.Decimal):
    """yaml serializable decimal"""

    yaml_tag = '!decimal'
    ledger = Ledger()

    def __new__(cls, value="0", context=None):
        self = super().__new__(cls, value, context)
        return self

    def __repr__(self):
        return f'cue.arithmetic.{super().__repr__()}'

    def __getitem__(self, key):
        """facilitate default zero on Data lookups"""
        return self

    @classmethod
    def to_yaml(cls, representer, node):
        return representer.represent_scalar(cls.yaml_tag, f'{node}')

    @classmethod
    def from_yaml(cls, constructor, node):
        return cls(node.value)

    @classmethod
    def atof(cls, value):
        """create a cue.arithemtic.Decimal from a localized string"""
        ledger = Decimal.ledger
        delocalized = (value.replace(' ', '')
                            .replace('%', '')
                            .replace(ledger['$'], '')
                            .replace(ledger['sep'], '')
                            .replace(ledger['dp_chr'], '.'))
        dec = cls(delocalized)
        if value.endswith('%'):
            dec = dec / 100
        return dec

    def quantize(self):
        """override quantize to return a cue.arithmetic.Decimal"""
        precision = Decimal(self.ledger['precision'])
        sup = super().quantize(precision, rounding_strategy)
        return Decimal(sup)


def journal_sum(items):
    """sum journal items"""
    total = (sum(i[-1].quantize() for i in items if i[0] == 'DR') -
             sum(i[-1].quantize() for i in items if i[0] == 'CR'))
    return Decimal(total)
