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

import requests, json, base64, time, configparser
from requests_oauthlib import OAuth2Session

from controller.authorize import Authorize
from controller.apirequests import apiRequest
from controller.db import db

class Pb:

    def setTransactionsbyIban(self,iban):
        try:
            #db().ibanExists(iban)
            payload = {
                'iban': iban,
                'limit': 200
            }
            endpoint = '/transactions/v2'
            res = apiRequest().makeRequest(payload,endpoint)
            db().insertTransactions(res)
        except:
            raise Exception("Could not find iban. Please provice iban and its credentials.")

    def setBank(self,bankdata):
        db().insertBank(bankdata)

    def setAccount(self,accountdata):
        db().insertAccount(accountdata)
