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

import dataset, json

from src.controller.base import Session, engine, Base

from src.model.transaction import Transaction
from src.model.account import Account
from src.model.iban import Iban

class db:
    def __init__(self):

        Base.metadata.create_all(engine)
        self.session = Session()

    def insertTransactions(self,transactions):
        try:
            for t in transactions['transactions']:
                newTransaction = Transaction(tid = t['id'], iban = t['originIban'], transaction = t)
                self.session.add(newTransaction)
            self.session.commit()
        except:
          raise Exception("Could not insert transaction")
        return 0

    def insertAccount(self,accountdata):
        # only deutsche bank
        #accountdata = json.loads(accountdata)
        usernameConcatenated = "/db" + accountdata['input_branch'] + accountdata['input_account'] + accountdata['input_subaccount']
        try:
            newAccount = Account(username = usernameConcatenated, password = accountdata['password'], bank = accountdata['bank'], access_token = accountdata['access_token'])
            newIbans = []
            for iban in accountdata['ibans']:
                newIbans.append(Iban(iban=iban['iban']))
            newAccount.ibans = newIbans
            self.session.add(newAccount)
            self.session.commit()
        except:
          raise Exception("Could not insert account")
        return 0

    def getAccountByIban(self, iban):
        account = self.session.query(Account) \
        .join(Iban, Account.ibans) \
        .filter(Iban.iban == iban) \
        .first()

        return account

    def setAccessTokenforAccount(self,username,access_token):
        res = self.session.query(Account).filter(Account.username == username).update({Account.access_token: access_token},synchronize_session='fetch')
        # if res  == 1
        self.session.commit()
        return 0
