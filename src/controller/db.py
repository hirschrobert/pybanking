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


from controller.base import engine, Session, Base

from model.transaction import Transaction
from model.account import Account
from model.iban import Iban
from model.bank import Bank


class db:

    def __init__(self):

        Base.metadata.create_all(engine)  # @UndefinedVariable
        self.session = Session()

    def insertTransactions(self, transactions):
        for t in transactions['transactions']:
            try:
                newTransaction = Transaction(tid=t['id'], iban=t['originIban'], transaction=t)
                self.session.merge(newTransaction)
                self.session.commit()
            except:
                self.session.rollback()
                print("transaction already exists")
                pass

    def insertAccount(self, accountdata):
        # only deutsche bank
        # accountdata = json.loads(accountdata)
        usernameConcatenated = "/db" + accountdata['input_branch'] + accountdata['input_account'] + accountdata['input_subaccount']
        try:
            newAccount = Account(username=usernameConcatenated, password=accountdata['password'], access_token={"hello":"world"})
            newAccount.bank = self.getBankByName(accountdata['bank'])
            newIbans = []
            for iban in accountdata['ibans']:
                newIbans.append(Iban(iban=iban))
            newAccount.ibans = newIbans
            self.session.add(newAccount)
            self.session.commit()
        except:
            self.session.rollback()
            raise Exception("Could not insert account")
            pass

    def insertBank(self, bankdata):
        try:
            newBank = Bank(
                bic=bankdata['bic'],
                name=bankdata['name'],
                authorize_endpoint=bankdata['authorize_endpoint'],
                tokenurl=bankdata['tokenurl'],
                apiurl=bankdata['apiurl'],
                requests=bankdata['requests']
            )
            self.session.add(newBank)
            self.session.commit()
        except:
            self.session.rollback()
            raise Exception("Could not insert bank")

    def getBankByName(self, name):
        bank = self.session.query(Bank) \
        .filter(Bank.name == name) \
        .first()

        return bank

    def getAccountByIban(self, iban):
        account = self.session.query(Account) \
        .join(Iban, Account.ibans) \
        .filter(Iban.iban == iban) \
        .first()

        return account

    def setAccessTokenforAccount(self, username, access_token):
        res = self.session.query(Account).filter(Account.username == username).update({Account.access_token: access_token}, synchronize_session='fetch')
        # if res  == 1
        self.session.commit()
        return 0
