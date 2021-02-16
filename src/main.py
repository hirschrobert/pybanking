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

from pybank import Pb
import argparse, sys


def license(args):
    if args.warranty:
        f = open('WARRANTY.md', 'r')
    elif args.copyright:
        f = open('LICENSE.md', 'r')
    print(f.read())
    f.close()

def transactions(args):
    if args.iban:
        Pb().setTransactionsbyIban(args.iban)


def parse_args():

    parser = argparse.ArgumentParser(description="stand up an lxc container")
    #parser.print_usage = parser.print_help

    parser.add_argument("-c", "--copyright", action='store_true', help="show copyright infos")
    parser.add_argument("-w", "--warranty", action='store_true', help="show warranty infos")

    parser.set_defaults(func=license)

    subparsers = parser.add_subparsers(help="sub command help")
    parser_ca = subparsers.add_parser("cash-accounts", help="get list of cash accounts by username and bank")
    parser_ca.add_argument("-u", "--username", required=True, action='store_true', help="show copyright infos")
    parser_ca.add_argument("-b", "--bank", action='store_true', help="show warranty infos")
    #parser_ca.set_defaults(func=Pb.getCashAccounts)
    parser_s = subparsers.add_parser("solvency", help="get solvency score of iban owner by iban")
    parser_s.add_argument("-i", "--iban", required=True, action='store', help="show copyright infos")
    #parser_s.set_defaults(func=Pb.getSolvencybyIban)
    parser_t = subparsers.add_parser("transactions", help="get transactions by iban")
    parser_t.add_argument("-i", "--iban", required=True, action='store', help="show copyright infos")
    parser_t.add_argument("--from", action='store_true', help="show copyright infos")
    parser_t.add_argument("--to", action='store_true', help="show copyright infos")
    parser_t.set_defaults(func=transactions)

    parsed_args = parser.parse_args()
    
    if len(sys.argv)==1:
        parser.print_help(sys.stderr)
        sys.exit(1)
        
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

    main()



    #Pb.setAccount(accountdata)
