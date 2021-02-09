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
from src.controller.db import db

from src.controller.authorize import Authorize

config = configparser.ConfigParser()
config.read('./config/db_api.ini') # change if necessary

client_id = config['db_api']['client_id']
client_secret = config['db_api']['client_secret']
redirect_uri = 'http://localhost'
authorize_endpoint = 'https://simulator-api.db.com/gw/oidc/authorize'
scope = {
    'offline_access',
    'read_customer_data',
    'read_transactions',
    'read_accounts',
    'transaction_notifications'
}
tokenurl = 'https://simulator-api.db.com/gw/oidc/token'
api = 'https://simulator-api.db.com/gw/dbapi/banking'

def tokenIsOutdated(creation_time,expires_in):
    if ((creation_time + expires_in) < int(time.time())):
        return True
    else:
        return False

def getAccessTokenByIban(iban):
    account = db().getAccountByIban(iban)
    access_token = account.getAccessToken()
    #TODO: also new token when scope changed
    if not hasattr(access_token , 'expires_in'):
        print("getting new token")
        access_token = Authorize(config).getNewAccessToken(account)
        db().setAccessTokenforAccount(account.getUsername(),access_token)
    elif (tokenIsOutdated(access_token['creation_time'],access_token['expires_in'])):
        print("refreshing token")
        access_token = Authorize(config).refreshToken(account)
        db().setAccessTokenforAccount(account.getUsername(),access_token)
    else:
        access_token = access_token
    return access_token

def makeRequest(payload,endpoint):
    apirequest = api + endpoint
    access_token = getAccessTokenByIban(payload['iban'])
    headers = {
        'Authorization': "Bearer " + access_token['access_token'],
        'Content-Type': "application/json; charset=utf-8"
    }
    r = requests.get(apirequest, headers=headers, params=payload)
    return json.loads(r.text)

def getTransactionsbyIban(iban):
    payload = {
        'iban': iban,
        'limit': 200
    }
    endpoint = '/transactions/v2'
    res = makeRequest(payload,endpoint)
    return res

print('''
pybanking Copyright (C) 2021 Robert Hirsch
This program comes with ABSOLUTELY NO WARRANTY; for details type \'show w\'.
This is free software, and you are welcome to redistribute it under certain conditions; type \'show c\' for details.
''')

iban = "DE10010000000000007549"
res = getTransactionsbyIban(iban)
db().insertTransactions(res)


"""
getAccessToken()

### only testdata
payload = {
    'iban': "DE10010000000000007549",
    'limit': 200
}
endpoint = '/transactions/v2'
res = makeRequest(payload,endpoint)

db().insertTransactions(res)

payload = {
    'iban': "DE10010000000000007549",
}
endpoint = '/customerSolvency/v1'
print(makeRequest(payload,endpoint))

payload = {}
endpoint = '/cashAccounts/v2'
print(makeRequest(payload,endpoint))
"""
