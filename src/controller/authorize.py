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

import requests, base64, time, json
from urllib import parse
from bs4 import BeautifulSoup
from requests_oauthlib import OAuth2Session

class Authorize:

    # Code
    def __init__(self,config):

        self.client_id = config['db_api']['client_id']
        self.client_secret = config['db_api']['client_secret']
        self.redirect_uri = 'http://localhost'
        self.authorize_endpoint = 'https://simulator-api.db.com/gw/oidc/authorize'
        self.scope = {
            'offline_access',
            'read_customer_data',
            'read_transactions',
            'read_accounts',
            'transaction_notifications'
        }
        self.tokenurl = 'https://simulator-api.db.com/gw/oidc/token'

    def getAuthorizationCode(self,account):

        str = account.getUsername()
        print(str)
        # Deutsche Bank specific
        prefix = str[:3]
        print(prefix)

        input_branch = str[3:6]
        print(input_branch)
        input_account = str[6:13]
        print(input_account)
        input_subaccount = str[13:15]
        print(input_subaccount)
        password = account.getPassword()

        oauth = OAuth2Session(self.client_id, redirect_uri=self.redirect_uri, scope=self.scope)
        authorization_url, state = oauth.authorization_url(self.authorize_endpoint)

        r = oauth.get(authorization_url)

        soup = BeautifulSoup(r.text,"lxml")
        try:
            csrf = soup.find('input', {'name': '_csrf'}).get('value')
        except:
            pass

        headers = {
            'Content-Type': "application/x-www-form-urlencoded",
            'cache-control': "no-cache"
        }
        form_data = {
                    "input_branch": input_branch,
                     "input_account": input_account,
                     "input_subaccount": input_subaccount,
                     "password": password,
                     "username": account.getUsername(),
                     "_csrf": csrf,
                     "submitButton": ""
        }
        r = oauth.post('https://simulator-api.db.com/gw/oidc/login', data=form_data, headers=headers,cookies=oauth.cookies,allow_redirects=False) # Login.
        r = oauth.get(r.headers['Location'],allow_redirects=False)
        params = dict(parse.parse_qsl(parse.urlsplit(r.headers['Location']).query))
        print(params)
        if (state == params['state']):
            return params['code']
        else:
            raise Exception("Could not retreive authorization code")
            return -1

    def getNewAccessToken(self, account):
        payload = {
            'grant_type': 'authorization_code',
            'code': self.getAuthorizationCode(account),
            'redirect_uri': self.redirect_uri
        }
        data_string = self.client_id + ":" + self.client_secret
        data_bytes = data_string.encode("utf-8")
        headers = {
            'Authorization': "Basic " + base64.b64encode(data_bytes).decode("utf-8"),
            'Content-Type': "application/x-www-form-urlencoded",
            'cache-control': "no-cache"
        }
        now = int(time.time())
        response = requests.post(self.tokenurl, data=payload, headers=headers)
        print(response.text)

        timeadd = { 'creation_time': now}
        jsonresult = json.loads(response.text)
        jsonresult.update(timeadd)
        return jsonresult

    def refreshToken(self, account):
        access_token = account.getAccessToken()
        data_string = self.client_id + ":" + self.client_secret
        data_bytes = data_string.encode("utf-8")
        headers = {
            'Authorization': "Basic " + base64.b64encode(data_bytes).decode("utf-8"),
            'Content-Type': "application/x-www-form-urlencoded"
        }
        payload = {
            'grant_type': 'refresh_token',
            'refresh_token': access_token['refresh_token'],
            'scope': " ".join(self.scope)
        }
        now = int(time.time())
        response = requests.post(self.tokenurl, data=payload, headers=headers)
        print(response.text)

        timeadd = { 'creation_time': now}
        jsonresult = json.loads(response.text)
        jsonresult.update(timeadd)
        return jsonresult
