import requests, json, base64, time, configparser
from requests_oauthlib import OAuth2Session

config = configparser.ConfigParser()
config.read('db_api.ini') # change if necessary

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
tokenfile = 'datadb.json'
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
    #print(r.text)
    jsonresult = json.loads(r.text)
    return json.dumps(jsonresult,indent=2)
    #with open(iban + '_transactions.json', 'w') as outfile:
    #    json.dump(jsonresult, outfile,indent=2)

getAccessToken()

### only testdata
payload = {
    'iban': "DE10010000000000007549",
}
endpoint = '/transactions/v2'
print(makeRequest(payload,endpoint))
payload = {
    'iban': "DE10010000000000007549",
}
endpoint = '/customerSolvency/v1'
print(makeRequest(payload,endpoint))

payload = {}
endpoint = '/cashAccounts/v2'
print(makeRequest(payload,endpoint))
