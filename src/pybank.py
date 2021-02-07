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
import db

config = configparser.ConfigParser()
config.read('./.config/db_api.ini') # change if necessary
tokenfile = './.config/access_token.json'

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

def init():
    oauth = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scope)
    authorization_url, state = oauth.authorization_url(authorize_endpoint)

    print('Bitte diese Seite im Browser öffnen und den sechstelligen Wert von \"code\" aus der Adresszeile kopieren und hier einfügen:\n', authorization_url)

    authorization_response = input('Bitte code eingeben: ')

    payload = {
        'grant_type': 'authorization_code',
        'code': authorization_response,
        'redirect_uri': redirect_uri
    }
    data_string = client_id + ":" + client_secret
    data_bytes = data_string.encode("utf-8")
    headers = {
        'Authorization': "Basic " + base64.b64encode(data_bytes).decode("utf-8"),
        'Content-Type': "application/x-www-form-urlencoded",
        'cache-control': "no-cache"
    }
    now = int(time.time())
    response = requests.post(tokenurl, data=payload, headers=headers)
    print(response.text)

    timeadd = { 'creation_time': now}
    jsonresult = json.loads(response.text)
    jsonresult.update(timeadd)
    with open(tokenfile, 'w') as outfile:
        json.dump(jsonresult, outfile,indent=2)
    return jsonresult['access_token']

def refreshToken(access_token_file):
    data_string = client_id + ":" + client_secret
    data_bytes = data_string.encode("utf-8")
    headers = {
        'Authorization': "Basic " + base64.b64encode(data_bytes).decode("utf-8"),
        'Content-Type': "application/x-www-form-urlencoded"
    }
    payload = {
        'grant_type': 'refresh_token',
        'refresh_token': access_token_file['refresh_token'],
        'scope': " ".join(scope)
    }
    now = int(time.time())
    response = requests.post(tokenurl, data=payload, headers=headers)
    print(response.text)

    timeadd = { 'creation_time': now}
    jsonresult = json.loads(response.text)
    jsonresult.update(timeadd)
    with open(tokenfile, 'w') as outfile:
        json.dump(jsonresult, outfile,indent=2)
    return jsonresult['access_token']

def tokenIsOutdated(creation_time,expires_in):
    if ((creation_time + expires_in) < int(time.time())):
        return True
    else:
        return False

def getAccessToken():
    with open(tokenfile, 'r') as outfile:
        access_token_file = json.load(outfile)
    #TODO: also new token when scope changed
    if (access_token_file.get('expires_in') == None):
        print("getting new token")
        access_token = init()
    elif (tokenIsOutdated(access_token_file['creation_time'],access_token_file['expires_in'])):
        print("refreshing token")
        access_token = refreshToken(access_token_file)
    else:
        access_token = access_token_file['access_token']
    return access_token

def makeRequest(payload,endpoint):
    apirequest = api + endpoint
    access_token = getAccessToken()
    headers = {
        'Authorization': "Bearer " + access_token,
        'Content-Type': "application/json; charset=utf-8"
    }
    r = requests.get(apirequest, headers=headers, params=payload)
    return json.loads(r.text)
    #jsonresult = json.loads(r.text)
    #return json.dumps(jsonresult,indent=2)
    #with open('./database/' + iban + '_transactions.json', 'w') as outfile:
    #    json.dump(jsonresult, outfile,indent=2)

print("pybanking  Copyright (C) 2021  Robert Hirsch\n
This program comes with ABSOLUTELY NO WARRANTY; for details type \'show w\'.\n
This is free software, and you are welcome to redistribute it
under certain conditions; type \'show c\' for details.")

getAccessToken()

### only testdata
payload = {
    'iban': "DE10010000000000007549",
    'limit': 200
}
endpoint = '/transactions/v2'
res = makeRequest(payload,endpoint)

db.insertTransactions(res)
# print("inserted")

"""
payload = {
    'iban': "DE10010000000000007549",
}
endpoint = '/customerSolvency/v1'
print(makeRequest(payload,endpoint))

payload = {}
endpoint = '/cashAccounts/v2'
print(makeRequest(payload,endpoint))
"""
