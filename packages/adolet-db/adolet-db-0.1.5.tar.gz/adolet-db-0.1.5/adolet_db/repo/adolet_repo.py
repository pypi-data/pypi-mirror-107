import os
import pickle
from typing import TypeVar
from adolet_db.repo.postgres_repo import PostgresRepo
from adolet_db.repo.cache_postgres_repo import cache_postgres_repo

POSTGRESREPO = TypeVar('PostgresRepo')
CACHE_FILE = 'cache_postgres_repo.cache'


def adolet_repo(email: str, api_key: str) -> POSTGRESREPO:
    if os.path.exists(CACHE_FILE):
        # Load cache
        with open(CACHE_FILE, 'rb') as handle:
            postgres_repo = pickle.load(handle)
            return postgres_repo

    else:
        # Instantiate and authenticate Postgres Repo
        postgres_repo = PostgresRepo(email=email, api_key=api_key)
        postgres_repo.authenticate_db()

        # Save cache in .pkl file
        cache_postgres_repo(postgres_repo=postgres_repo)
        return postgres_repo
