## Alphaversion!!

## pybank [![](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

### backend client for banking api (Deutsche Bank)

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
