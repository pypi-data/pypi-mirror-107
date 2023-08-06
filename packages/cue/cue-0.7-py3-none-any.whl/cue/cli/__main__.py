# cue
# Accounting system for Linux
# Copyright (c) 2021 Kosciuszko Cloud
# Open source, MIT license: http://www.opensource.org/licenses/mit-license.php
"""
CLI commands

"""
import types, argparse, locale
from pathlib import Path

locale.setlocale(locale.LC_ALL, '') # '' -> ledger['locale']), hmmm

def init(*args):
    """initialise a cue ledger - part 1"""
    from cue.ledger import Ledger
    Ledger.boilerplate()

def commit(*args):
    """process temp files"""
    for path in Path().glob('**/temp__*'):
        cls_name = path.stem.split('__')[1]
        if cls_name == 'Ledger':
            from cue.ledger import Ledger
            Ledger.commit()
        elif cls_name == 'Invoice':
            from cue.invoice import Invoice
            invoice = Invoice.parse(path)
            invoice.issue()

def invoice(*args):
    """invoice a customer"""
    from cue.invoice import Invoice
    customer = ' '.join(args)
    Invoice.boilerplate(customer)

def clean(*args):
    """remove cue ledger from dir or parent"""
    from cue.ledger import Ledger
    Ledger().clean()

def cat(*args):
    """respresent the item using ascii art"""
    path = Path(args[0])
    if path.suffix == '.acc':
        from cue.account import Account
        item = Account(path)
    else:
        item = path.read_text()
    print(str(item))

def echo(*args):
    """echo args"""
    print(' '.join(args))

commands = [k for k, v in globals().items() if
            type(v) == types.FunctionType]

parser = argparse.ArgumentParser(prog='cue')
parser.add_argument('command', choices=commands)
parser.add_argument('args', nargs=argparse.REMAINDER)
args = parser.parse_args()
func = globals()[args.command]
func(*args.args)
