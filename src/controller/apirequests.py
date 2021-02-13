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

import requests, json
from controller.db import db
from controller.authorize import Authorize

class apiRequest:

    def __init__(self):
        self.api = 'https://simulator-api.db.com/gw/dbapi/banking'

    def tokenIsOutdated(self,creation_time,expires_in):
        if ((creation_time + expires_in) < int(time.time())):
            return True
        else:
            return False

    def getAccessTokenByIban(self,iban):
        account = db().getAccountByIban(iban)
        access_token = account.getAccessToken()
        #TODO: also new token when scope changed
        if not hasattr(access_token , 'expires_in'):
            print("getting new token")
            access_token = Authorize().getNewAccessToken(account)
            db().setAccessTokenforAccount(account.getUsername(),access_token)
        elif (tokenIsOutdated(access_token['creation_time'],access_token['expires_in'])):
            print("refreshing token")
            access_token = Authorize().refreshToken(account)
            db().setAccessTokenforAccount(account.getUsername(),access_token)
        else:
            access_token = access_token
        return access_token

    def makeRequest(self,payload,endpoint):
        apirequest = self.api + endpoint
        access_token = self.getAccessTokenByIban(payload['iban'])
        headers = {
            'Authorization': "Bearer " + access_token['access_token'],
            'Content-Type': "application/json; charset=utf-8"
        }
        r = requests.get(apirequest, headers=headers, params=payload)
        return json.loads(r.text)
