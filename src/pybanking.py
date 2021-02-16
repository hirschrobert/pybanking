#!/usr/bin/env python3
# -*- Mode:Python; encoding:utf8 -*-
#
# pybanking - a banking backend client at your service
# Copyright (C) 2021  Robert Hirsch <dev@robert-hirsch.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

import json, argparse, sys
from controller.apirequests import apiRequest  # @UnresolvedImport
from controller.db import db  # @UnresolvedImport

from model.bankapi import Model


class Pb:
    
    def __init__(self):
        print("pybanking Copyright (C) 2021 Robert Hirsch")
        print("This program comes with ABSOLUTELY NO WARRANTY; for details type \'-w\'.")
        print("This is free software, and you are welcome to redistribute it under certain conditions; type \'-c\' for details.")
    
    def connect(self):
        self.db = db()
        with open('../config/bankdata.json', 'r') as f:
            data = json.load(f)
            for bankdata in data:
                try:
                    self.setBank(bankdata)
                except:
                    print("not inserting bank, already exist")
                    pass
        
            
        accountdata = {
            "input_branch": "100",
            "input_account": "",
            "input_subaccount": "00",
            "password": "",
            "bank": "Deutsche Bank",
            "bic": "DEUTDEDB110",
            "ibans": [""]
        }
    
        self.setAccount(accountdata)

    def license(self, args):
        if args.warranty:
            f = open('WARRANTY.md', 'r')
        elif args.copyright:
            f = open('LICENSE.md', 'r')
        print(f.read())
        f.close()
    
    def pybanking_args(self, args):
        d = vars(args)
        print(d)
        self.connect()
        if d['pybanking'] == 'transactions':
            self.setTransactionsbyIban(d['iban'], d['from'], d['to'])
        elif d['pybanking'] == 'add-bank-account':
            try:
                bank = self.db.getBankByBic(d['bic'])
                accountdata = {}
                accountdata['bic'] = d['bic']
                print(bank.getAccountInput())
                for k, v in bank.getAccountInput().items():
                    accountdata[k] = input(v + ": ")
            except:
                raise Exception("could not find bank by bic")
            print(bank.name)
            print(accountdata)
            bankmodel = Model(bank)
            res = bankmodel.insertUserAccount(accountdata)
            self.db.insertAccount(res)
        elif args.cashAccounts:
            self.getCashAccounts(args.cashAccounts.iban)
        elif args.solvency:
            self.getSolvencybyIban(args.solvency.iban)
 
    def parse_args(self):
    
        parser = argparse.ArgumentParser(description="pybanking help menu")
        # parser.print_usage = parser.print_help
    
        parser.add_argument("-c", "--copyright", action='store_true', help="show copyright infos")
        parser.add_argument("-w", "--warranty", action='store_true', help="show warranty infos")
    
        parser.set_defaults(func=self.license)
    
        subparsers = parser.add_subparsers(help="sub command help", dest="pybanking")
        parser_ba = subparsers.add_parser("add-bank-account", help="adds bank account by bic")
        parser_ba.add_argument("--bic", required=True, action='store', help="show warranty infos")
        parser_ba.set_defaults(func=self.pybanking_args)
        parser_ca = subparsers.add_parser("cash-accounts", help="get list of cash accounts by username and bank")
        parser_ca.add_argument("-u", "--username", required=True, action='store', help="show copyright infos")
        parser_ca.add_argument("-b", "--bank", action='store', help="show warranty infos")
        parser_ca.set_defaults(func=self.pybanking_args)
        parser_s = subparsers.add_parser("solvency", help="get solvency score of iban owner by iban")
        parser_s.add_argument("--iban", required=True, action='store', help="show copyright infos")
        parser_s.set_defaults(func=self.pybanking_args)
        parser_t = subparsers.add_parser("transactions", help="get transactions by iban")
        parser_t.add_argument("--iban", required=True, action='store', help="show copyright infos")
        parser_t.add_argument("--from", action='store', help="booking date of original transaction from what date to be searched for. Date in ISO 8601 format, YYYY-MM-DD. If not provided, all accessible transactions are called (usually the last 13 month).")
        parser_t.add_argument("--to", action='store', help="booking date until which the transactions to be searched for. Date in ISO 8601 format YYYY-MM-DD. If not provided, the current day will be chosen. bookingDateTo must be greater than or equal to bookingDateFrom.")
        parser_t.set_defaults(func=self.pybanking_args)
    
        parsed_args = parser.parse_args()
        
        if len(sys.argv) == 1:
            parser.print_help(sys.stderr)
            sys.exit(1)
        
        parsed_args.func(parsed_args)
    
        return parser.parse_known_args()
    
    # params: iban, from, to
    def setTransactionsbyIban(self, iban, *args):
        params = {
            'iban': iban,
            'from': args[0],
            'to': args[1]
        }
        print("from: ", args[0])
        print("to: ", args[1])
        try:
            bank = self.db.getBankByIban(iban)
            bankmodel = Model(bank)
            endpoint, payload = bankmodel.userArgsToModelParams(self.setTransactionsbyIban.__name__, params)
            res = apiRequest().makeRequest(payload, endpoint)
            self.db.insertTransactions(res)
        except:
            raise Exception("Could not find iban. Please provide iban and its credentials.")

    def setBank(self, bankdata):
        self.db.insertBank(bankdata)

    def setAccount(self, accountdata):
        try:
            self.db.insertAccount(accountdata)
        except:
            print("not inserting account, already exist")
            pass
