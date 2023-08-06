# cue
# Accounting system for Linux
# Copyright (c) 2021 Kosciuszko Cloud
# Open source, MIT license: http://www.opensource.org/licenses/mit-license.php
"""
Ledger

"""
import shutil
from pathlib import Path
from collections import OrderedDict

from ruamel.yaml import YAML


class Ledger(OrderedDict):
    """a ledger for an organization"""

    def __init__(self):
        """parse the settings file"""
        self.path, self.settings_path = self.get_paths()
        settings = yaml.load(self.settings_path)
        super().__init__(**settings)

    @classmethod
    def clean(cls):
        """remove cue files from dir"""
        shutil.rmtree('.cue')
        for acc_path in Path().glob('*.acc'):
            acc_path.unlink()

    def get_paths(self):
        """locate the ledger and settings"""
        here = Path().resolve()
        for path in [here] + list(here.parents):
            if (path / '.cue').exists():
                settings_path = path / '.cue' / 'settings.yml'
                return path, settings_path
        raise EnvironmentError('not a cue ledger')

    def dump(self):
        """save to file in !!omap form"""
        yaml.dump(OrderedDict(self), self.settings_path)


yaml = YAML()
