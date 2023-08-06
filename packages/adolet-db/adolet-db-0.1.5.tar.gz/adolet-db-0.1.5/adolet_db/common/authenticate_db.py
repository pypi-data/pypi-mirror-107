import requests
from typing import Any, Dict


def authenticate_db(email: str, api_key: str) -> Dict[str, Any]:
    params = {'email': email, 'api_key': api_key}
    res = requests.get(
        'http://api.postgres.adolet.com/authenticate-db-api',
        params=params,
    )
    res = res.json()
    return res
