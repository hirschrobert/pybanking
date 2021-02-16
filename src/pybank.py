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

import json
from controller.apirequests import apiRequest  # @UnresolvedImport
from controller.db import db  # @UnresolvedImport


class Pb:
    
    def __init__(self):
        self.db = db()
        with open('../config/bankdata.json', 'r') as f:
            data = json.load(f)
            for bankdata in data:
                try:
                    self.setBank(bankdata)
                except:
                    print("not inserting bank, already exist")
                    pass


    def setTransactionsbyIban(self, iban):
        try:
            # db().ibanExists(iban)
            payload = {
                'iban': iban,
                'limit': 200
            }
            endpoint = '/transactions/v2'
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
