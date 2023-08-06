import pickle
from typing import TypeVar

POSTGRESREPO = TypeVar('PostgresRepo')
CACHE_FILE = 'cache_postgres_repo.cache'


def cache_postgres_repo(postgres_repo: POSTGRESREPO) -> bool:
    '''Save the Postgres Repo class instance in a .pkl which will in essence act like a cache'''
    # Save cache in .pkl file
    with open(CACHE_FILE, 'wb') as handle:
        pickle.dump(
            postgres_repo,
            handle,
            protocol=pickle.HIGHEST_PROTOCOL,
        )
    print("SUCCESS - Cache has beeen saved")
    return True
