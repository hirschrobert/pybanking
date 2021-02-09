[![](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/) ![CodeQL](https://github.com/hirschrobert/pybanking/workflows/CodeQL/badge.svg?branch=main)
## Alphaversion!!

## pybanking - a backend banking client at your service

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
- BeautifulSoup
- configparser
- dataset
- json
- requests
- requests_oauthlib (OAuth2Session)
- sqlalchemy
- time
