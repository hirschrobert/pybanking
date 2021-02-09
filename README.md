[![](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/) ![CodeQL](https://github.com/hirschrobert/pybanking/workflows/CodeQL/badge.svg?branch=main)
## Alphaversion!!

## pybanking - a backend banking client at your service

[Deutsche Bank Api reference](https://developer.db.com/)

rename file 'db_api.ini.sample' in folder 'config' into 'db_api.ini' and replace values with your individual credentials:

```
[db_api]
client_id = put_your_client_id_here
client_secret = put_your_client_secret_here
```

python dependencies:
- beautifulsoup4>=4.8.2
- dataset>=1.4.4
- lxml>=4.5.0
- oauthlib>=3.1.0
- requests>=2.22.0
- requests-oauthlib>=1.3.0
- SQLAlchemy>=1.3.23
- urllib3>=1.25.8
