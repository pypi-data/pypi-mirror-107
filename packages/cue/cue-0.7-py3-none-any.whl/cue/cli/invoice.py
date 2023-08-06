# cue
# Accounting system for Linux
# Copyright (c) 2021 Kosciuszko Cloud
# Open source, MIT license: http://www.opensource.org/licenses/mit-license.php
"""
CLI invoice parser and constructors

"""
import re
from pathlib import Path
from collections import defaultdict, OrderedDict
from datetime import date

from ruamel.yaml import YAML

import cue.invoice, cue.data
from cue.ledger import Ledger
from cue.arithmetic import Decimal
from cue.journal import Journal
from cue.cli.account import sanitize_

code = Path(__file__).parent
yaml = YAML()


class Invoice(cue.invoice.Invoice):
    """invoice parser and constructors"""

    ledger = Ledger()

    @classmethod
    def boilerplate(cls, customer):
        """step 1 - drop a boilerplate file into the cwd"""
        target = Path(f'temp__Invoice__{customer}.txt')
        params = {
            'org_name': cls.ledger['org_name'],
            'tagline': cls.ledger['tagline'],
            'date': date.today(),
            'customer': customer,
            'taxes': '\n'.join([f'{" ":>60}{k}  {cls.ledger["$"]}0.00'
                                for k in
                                cls.ledger['transaction_taxes']]),
            '$': cls.ledger['$'],
            'terms': cls.ledger['terms']
        }
        template = code / 'templates' / 'invoice.txt'
        content = template.read_text().format(**params)
        target.write_text(content)

    @classmethod
    def parse(cls, temp_path):
        """interpret invoice data from the edited file"""
        curr_sign = cls.ledger['$']
        if curr_sign == '$':
            curr_sign = r'\$'
        re_ = re.compile(token_str.format(curr_sign), re.DOTALL)
        tokens = cls.tokenize(re_, temp_path)
        data = cue.data.Data()

        # some of the values we want to harvest from the
        # tokens are scalar, so we can access them through a
        # dict
        tokend = dict(tokens)
        data['number'] = int(tokend['NUM'])
        data['date'] = date.fromisoformat(tokend['DATE'])
        data['customer'] = temp_path.stem.split('__')[-1]
        data['billing_address'] = tokend['ADDR']

        # item values are consecutive combinations of CODE,
        # DESC, UNIT, and QTY tokens. CODE and UNIT might be
        # missing depending on what kind of item it is, so we
        # get all the DESC tokens, which are present for
        # every item, and parse the tokens around them
        desc_index = (i for i, (typ, tok)
                      in enumerate(tokens)
                      if typ == 'DESC')
        item_tokens = [list(tokens[i - 1:i + 3])
                       for i in desc_index]

        # then fix some edge cases...
        for i, item in enumerate(item_tokens[:]):
            prev_typ, prev_tok = item[0]
            next_typ, next_tok = item[2]

            # the token before the DESC should be a CODE, and
            # the token after the DESC should be a UNIT
            # price. If the previous token is not a CODE, we
            # got the last token from the previous item, or
            # something else irrelevant, so replace that
            # token with an empty CODE
            if prev_typ != 'CODE':
                item_tokens[i] = [('CODE', '')] + item[1:]

            # if the next token is not a UNIT, we got some
            # number value that was tokenized as a QTY, but
            # that's not what it really meant. It meant we
            # didn't want to have units for that line item,
            # just a price. So capture the value from that
            # token and reframe it as a single UNIT
            if next_typ != 'UNIT':
                item_tokens[i] = item_tokens[i][:2] + [('UNIT', next_tok),
                                                       ('QTY', '1')]

        # dictify and store the items
        data['items'] = [OrderedDict([(k.lower(), v) for k, v in item])
                         for item in item_tokens]

        # calculate and append item totals
        for item in data['items']:
            total = Decimal(Decimal.atof(item['unit']) *
                            Decimal.atof(item['qty'])).quantize()
            item['total'] = total

        # calculate the subtotal
        data['subtotal'] = Decimal(sum(item['total'] for item
                                       in data['items']))

        # handle shipping and discount if any
        if 'SHIP' in tokend:
            data['shipping'] = cls._parse_mod(tokend['SHIP'], 0)
        if 'DIS' in tokend:
            data['discount'] = cls._parse_mod(tokend['DIS'],
                                              data['subtotal'])

        # calculate the invoice total excluding taxes
        data['total_ex'] = Decimal(data['subtotal'] 
                                   + data['shipping']['amt']
                                   - data['discount']['amt'])

        # handle taxes if any
        labels = [tok for typ, tok in tokens if typ == 'LABEL']
        data['taxes'] = cls._parse_taxes(labels, data['total_ex'])

        # calculate the invoice total
        data['total'] = Decimal(data['total_ex'] +
                                sum(data['taxes'].values()))

        # generate the invoice
        invoice = cls(customer=data['customer'], data=data)
        invoice.temp_path = temp_path
        return invoice

    @classmethod
    def tokenize(cls, re_, path):
        """tokenize the edited file"""
        tokens = []
        pos = 0
        text = path.read_text()
        match = re_.match(text)
        ignore = ('WORD', 'GAP', 'CRUD', 'TOP', 'DLR', 'EOF', 'HEAD')
        while pos < len(text):
            typ = match.lastgroup
            if typ in ignore:
                pos = max(match.end(), pos + 1)
            else:
                tok = match.group(typ).strip()
                tokens.append((typ, tok))
                pos = match.end()
            match = re_.match(text, pos)
        return tuple(tokens)

    @classmethod
    def _parse_taxes(cls, labels, total_ex):
        """parse and calculate tax amounts"""
        taxes = OrderedDict([(k, v) for k, v in
                             cls.ledger['transaction_taxes'].items()
                             if k in labels])
        for k, v in taxes.items():
            tax_rate = Decimal.atof(v)
            tax = Decimal(tax_rate * total_ex).quantize()
            taxes[k] = tax
        return taxes

    @classmethod
    def _parse_mod(cls, token, subtotal):
        """discounts, coupons and shipping"""
        label, value = token.strip().split()
        if value.endswith('%'):
            label += ' {}'.format(value)
            actual = Decimal(Decimal(value.strip('%'))
                             * ONE_PERCENT
                             * subtotal).quantize()
        else:
            actual = Decimal.atof(value).quantize()
        return OrderedDict([('label', label),
                            ('amt', actual)])

    def issue(self):
        """assign a sequential number, save, post if auto"""
        self['number'] = self.get_next()
        self.dump()
        self.temp_path.unlink()
        if self.ledger['posting'] == 'auto':

            # journalize the invoice individually and post the journal
            ar = {k:f'{sanitize_(v)}.acc' for k, v in
                  self.ledger['ar_config'].items()}
            msg = f'inv #{self["number"]:>6} - {self["customer"]}'
            items = [
                ('DR', ar['ar'], msg, self['total']),
                ('CR', ar['revenue'], msg, self['total_ex'])
            ]
            for tax_label, tax_amt in self['taxes'].items():
                tax_msg = f'inv #{self["number"]:>6} - {tax_label}'
                tax_item = ('CR', ar[tax_label], tax_msg, tax_amt)
            items.append(tax_item)
            j = OrderedDict(items=items, posted=False)
            journal = Journal(data=j)
            journal.dump()
            journal.post()

            # move invoice to .cue/posted
            path = self.path
            new_parent = self.ledger.path / '.cue' / 'posted'
            self.path = path.rename(new_parent / path.name)
            self.protect()


def get_address(org, addr_type):
    """look up customer/vendor address"""
    for org_type in ('customers', 'vendors'):
        fname = os.path.join(CUE_DIR, org_type, '{}.yml'.format(org))
        try:
            with open(fname, 'r') as f:
                data = load(f.read())
            address_field = '{}_address'.format(addr_type)
            return data[address_field].strip()
        except FileNotFoundError:
            pass
    return ''

def update_address(org, addr_type, filename):
    """create or update billing address if changed"""
    existing = get_address(org, addr_type)
    fname = os.path.join(INSTANCE_DIR, 'current', filename)
    cls, org_type = ([VendorInvoice, 'vendors']
                     if addr_type == 'remittance'
                     else [Invoice, 'customers'])
    doc = cls(fname)
    address_field = '{}_address'.format(addr_type)
    new_addr = doc.meta[address_field]
    if new_addr != existing:
        org_fname = os.path.join(CUE_DIR, org_type, '{}.yml'.format(org))
        with open(org_fname, 'w') as f:
            f.write(dump({address_field: new_addr}))
        return ('{} updated'.format(address_field) if existing else
                'created {}: {}'.format(org_type[:-1], org))


# tokenizer inputs

tok_spec = yaml.load(code / 'templates' / 'token_spec.yml')
iter_tok_spec = ((dd[k]
                  for k in [
                      'lookbehind',
                      'tag',
                      'pattern',
                      'lookahead'
                  ])
                 for dd in [
                     defaultdict(str, d)
                     for d in tok_spec
                 ])
tok_fmt = '{}(?P<{}>{}){}'
token_str = '|'.join(tok_fmt.format(*s) for s in iter_tok_spec)
