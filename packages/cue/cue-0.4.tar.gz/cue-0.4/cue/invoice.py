# cue
# Accounting system for Linux
# Copyright (c) 2021 Kosciuszko Cloud
# Open source, MIT license: http://www.opensource.org/licenses/mit-license.php
"""
Invoice

"""
from pathlib import Path
from datetime import datetime

from cue.data import Data


class Invoice(Data):
    """an invoice"""

    def __init__(self, filename=None, customer=None, data=None):
        if filename:
            path = Path(filename)
        else:
            ts = f'{datetime.now():%Y%m%d%H%M%S}'
            filename = f'{ts}-{customer}.inv'
            path = Path('.cue') / 'current' / filename
        super().__init__(path, data)
