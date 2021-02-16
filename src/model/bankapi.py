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

class Model():
    
    def __init__(self, bank):
        self.bank = bank
    
    def userArgsToModelParams(self, method, userparams):
        if method == 'setTransactionsbyIban':
            userparams['limit'] = '200'
            endpoint = self.bank.requests['transactions']['endpoint']
            bankparams = self.bank.requests['transactions']['params']
            print(self.bank.requests['transactions']['params'])
            payload = {}
            for k, v in bankparams.items():
                print(k + ">" + v[0])
                if k in userparams:
                    payload[v[0]] = userparams[k]
                    userparams.pop(k)
            print(userparams)
            if userparams:
                raise Exception("user input does not match api structure: ", userparams) 
                pass
            print(payload)
            return endpoint, payload
        
    
    def insertUserAccount(self, accountdata):
        # usernameConcatenated is only Deutsche Bank, needs to be decoupled
        if not 'username' in accountdata:
            accountdata['username'] = "/db" + accountdata['input_branch'] + accountdata['input_account'] + accountdata['input_subaccount']
        res = {
            "username": accountdata['username'],
            "password": accountdata['password'],
            "ibans": accountdata['ibans'].split(","),
            "bic": accountdata['bic']
            }
        
        return res
        