##Alphaversion!!

##backend client for banking api (Deutsche Bank)

create config file 'db_api.ini' with this content:

```
[db_api]
client_id = secret_client_id
client_secret = secret_client_secret
```

python dependencies:
- base64
- configparser
- json
- requests
- requests_oauthlib (OAuth2Session)
- time
