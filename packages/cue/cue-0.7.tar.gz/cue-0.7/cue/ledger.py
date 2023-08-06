# cue
# Accounting system for Linux
# Copyright (c) 2021 Kosciuszko Cloud
# Open source, MIT license: http://www.opensource.org/licenses/mit-license.php
"""
Ledger

"""
import shutil, re
from pathlib import Path
from collections import OrderedDict

from ruamel.yaml import YAML

code = Path(__file__).parent


class Ledger(OrderedDict):
    """a ledger for an organization"""

    def __init__(self):
        """parse the settings file"""
        self.path, self.settings_path = self.get_paths()
        settings = yaml.load(self.settings_path)
        super().__init__(**settings)

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

    @classmethod
    def boilerplate(cls):
        """step 1 - drop a boilerplate file into the cwd"""
        verify_not_existing_ledger()
        here = Path().resolve()
        params = {
            'org_name': here.stem
        }
        template = code / 'cli' / 'templates' / 'settings.yml'
        content = template.read_text().format(**params)
        target = here / 'temp__Ledger__settings.yml'
        target.write_text(content)

    @classmethod
    def commit(cls):
        """step 2 - process the edited file and setup the ledger"""
        make_dirs()
        temp_path = Path('temp__Ledger__settings.yml')
        settings_path = Path('.cue') / 'settings.yml'
        make_settings_file(temp_path, settings_path)
        ledger = cls()
        make_ledger(ledger)
        return ledger

    @classmethod
    def wizard(cls):
        """make a new ledger using the wizard"""

    @classmethod
    def clean(cls):
        """remove cue files from dir"""
        shutil.rmtree('.cue')
        for acc_path in Path().glob('*.acc'):
            acc_path.unlink()


yaml = YAML()

def verify_not_existing_ledger():
    """verify there's not an existing ledger here"""
    try:
        ledger = Ledger()
    except EnvironmentError:
        pass
    else:
        msg = f'Existing ledger in {ledger.path}. Aborting'
        raise EnvironmentError(msg)

def make_dirs():
    """create the dir structure for source docs, etc"""
    app_path = Path('.cue')
    paths = [app_path / 'current',
             app_path / 'posted',
             app_path / 'customers']
    for path in paths:
        path.mkdir(parents=True)

def make_settings_file(source_path, dest_path):
    """create the ledger settings file"""
    with source_path.open() as f:
        with dest_path.open('a') as outf:
            for line in f:
                compact_line = re.sub('\s*#.*', '', line.rstrip())
                if compact_line.strip():
                    print(compact_line, file=outf)
                    print(compact_line)
    source_path.unlink()

def make_ledger(ledger):
    """create accounts and opening journal if any"""
    from cue.arithmetic import Decimal
    from cue.account import Account
    from cue.journal import Journal
    coa = [{'bal_type': ledger['account_types'][typ],
            'title': account if type(account) is str
                     else list(account.keys())[0],
            'bal': 0 if type(account) is str
                   else list(account.values())[0]}
           for typ, accounts in
           ledger['starting_accounts'].items()
           for account in accounts]
    opening_items = []
    for acc in coa:
        a = Account.create(acc['title'], acc['bal_type'])
        if acc['bal']:
            item = (a['bal_type'], a.path.name, 'Opening balance',
                    Decimal(acc['bal']).quantize())
            opening_items.append(item)
        a.dump()
    if opening_items:
        j = OrderedDict(items=opening_items,
                        posted=False)
        journal = Journal(data=j)
        journal.dump()
        journal.post()
