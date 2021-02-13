#!/usr/bin/env python3
# -*- Mode:Python; encoding:utf8 -*-
#
# pybanking - a banking backend client at your service
# Copyright (C) 2021  Robert Hirsch <info@robert-hirsch.de>
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

from pybank import Pb
import argparse
import sys

def license(value):
    if value == "warranty":
        f = open('WARRANTY.md', 'r')
    else:
        f = open('LICENSE.md', 'r')
    print(f.read())
    f.close()

def do_function(args):
    if args.iban:
        print(args.iban)

def parse_args():

    parser = argparse.ArgumentParser(description="stand up an lxc container")
    parser.print_usage = parser.print_help

    parser.add_argument("-c", "--copyright", action='store_true', help="show copyright infos")
    parser.add_argument("-w", "--warranty", action='store_true', help="show warranty infos")

    parser.set_defaults(func=do_function)

    subparsers = parser.add_subparsers(help="sub command help")
    parser_ca = subparsers.add_parser("cash-accounts", help="get list of cash accounts by username and bank")
    parser_ca.add_argument("-u", "--username", required=True, action='store_true', help="show copyright infos")
    parser_ca.add_argument("-b", "--bank", action='store_true', help="show warranty infos")
    parser_ca.set_defaults(func=do_function)
    parser_s = subparsers.add_parser("solvency", help="get solvency score of iban owner by iban")
    parser_s.add_argument("-i", "--iban", required=True, action='store', help="show copyright infos")
    parser_s.set_defaults(func=Pb().getTransactionsbyIban)
    parser_t = subparsers.add_parser("transactions", help="get transactions by iban")
    parser_t.add_argument("-i", "--iban", required=True, action='store_true', help="show copyright infos")
    parser_t.add_argument("--from", action='store_true', help="show copyright infos")
    parser_t.add_argument("--to", action='store_true', help="show copyright infos")
    parser_t.set_defaults(func=do_function)

    parsed_args = parser.parse_args()
    parsed_args.func(parsed_args)

    return parser.parse_known_args()

def main():
    args, unknown = parse_args()

if __name__ == "__main__":
    print('''
pybanking Copyright (C) 2021 Robert Hirsch
This program comes with ABSOLUTELY NO WARRANTY; for details type \'-w\'.
This is free software, and you are welcome to redistribute it under certain conditions; type \'-c\' for details.
    ''')

    #main()

    bankdata = {
        "name": "Deutsche Bank",
        "authorize_endpoint": "https://simulator-api.db.com/gw/oidc/authorize",
        "tokenurl": "https://simulator-api.db.com/gw/oidc/token",
        "apiurl": "https://simulator-api.db.com/gw/dbapi/banking",
        "requests": {
            "cashAccounts": {
                "endpoint": "/cashAccounts/v2",
                "params": {
                    "optional": "limit",
                    "optional": "offset"
                }
            },
            "customerSolvency": {
                "endpoint": "/customerSolvency/v1",
                "params": {
                    "required": "iban"
                }
            },
            "transactions": {
                "endpoint": "/transactions/v2",
                "params": {
                    "required": "iban",
                    "optional": "bookingDateFrom",
                    "optional": "bookingDateTo",
                    "optional": "limit",
                    "optional": "offset"
                }
            }
        }

    }
    Pb().setBank(bankdata)


    accountdata = {
        "input_branch": "100",
        "input_account": "1005249",
        "input_subaccount": "00",
        "password": "",
        "bank": "Deutsche Bank",
        "ibans": [""]
    }
    Pb().setAccount(accountdata)
    Pb().setTransactionsbyIban('')


"""
#python main.py -t -i de12123456 --from 20200101 --to 20200131
Pb().getTransactionsbyIban(args.iban)
#python main.py -s -i de12123456
Pb().getCustomerSolvencybyIban(args.iban)
#python main.py -ca -u max.mustermann -b "Deutsche Bank"
Pb().getCashAccounts(args.username)
"""
