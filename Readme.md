[![](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
## Alphaversion!!

## pybank

### backend client for banking api (Deutsche Bank)

[Deutsche Bank Api reference](https://developer.db.com/)

create config file 'db_api.ini' with this content:

```
[db_api]
client_id = put_your_client_id_here
client_secret = put_your_client_secret_here
```

python dependencies:
- base64
- configparser
- json
- requests
- requests_oauthlib (OAuth2Session)
- time
