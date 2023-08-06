import requests
import pickle
import os
from typing import Dict, Any, TypeVar, List
from adolet_db.common import is_args_none

CACHE_FILE = 'cache_postgres_repo.cache'


class PostgresRepo:
    def __init__(
        self,
        dbname: str,
        user: str,
        password: str,
        host: str,
        port: int,
    ):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.URL = 'http://api.postgres.adolet.com'

    def clear_cache(self) -> bool:
        if os.path.exists(CACHE_FILE):
            os.remove(CACHE_FILE)
            print("SUCCESS - Cache has been cleared")
            return True

        print("FAILURE - There is no cache to be clear")
        return False

    def dt(self) -> List[str]:
        is_args_none(args=list(locals().values()))
        try:
            params = {
                'dbname': self.dbname,
                'user': self.user,
                'password': self.password,
                'host': self.host,
                'port': self.port,
            }

            res = requests.get(f'{self.URL}/dt-api', params=params)
            res: Dict[str, Any] = res.json()
            return res

        except:
            raise Exception(
                "There is an error with .dt() in postgres_repo.py - You may need to call .clear_cache()"
            )

    def get_columns(self, table_name: str) -> List[str]:
        is_args_none(args=list(locals().values()))
        try:
            params = {
                'dbname': self.dbname,
                'user': self.user,
                'password': self.password,
                'host': self.host,
                'port': self.port,
                'table_name': table_name,
            }

            res = requests.get(f'{self.URL}/get-columns-api', params=params)
            res: Dict[str, Any] = res.json()
            return res

        except:
            raise Exception(
                "There is an error with .get_columns() in postgres_repo.py - You may need to call .clear_cache()"
            )

    def get_table_schema(self, table_name: str) -> Dict[str, str]:
        is_args_none(args=list(locals().values()))
        try:
            params = {
                'dbname': self.dbname,
                'user': self.user,
                'password': self.password,
                'host': self.host,
                'port': self.port,
                'table_name': table_name,
            }

            res = requests.get(
                f'{self.URL}/get-table-schema-api',
                params=params,
            )
            res: Dict[str, Any] = res.json()
            return res

        except:
            raise Exception(
                "There is an error with .get_table_schema() in postgres_repo.py - You may need to call .clear_cache()"
            )

    def insert(self, table_name: str, dto: Dict[str, Any]) -> Dict[str, Any]:
        is_args_none(args=list(locals().values()))
        try:
            if 'id' in dto: dto.pop('id')

            params = {
                'dbname': self.dbname,
                'user': self.user,
                'password': self.password,
                'host': self.host,
                'port': self.port,
                'table_name': table_name,
                'columns': list(dto.keys()),
                'values': list(dto.values()),
            }

            res = requests.get(f'{self.URL}/insert-api', params=params)
            res = res.json()
            return res

        except:
            raise Exception(
                "There is an error with .insert() in postgres_repo.py - You may need to call .clear_cache()"
            )

    def insert_many(
        self,
        table_name: str,
        dtos: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        pass

    def delete(self, table_name: str, id: int) -> Dict[str, Any]:
        is_args_none(args=list(locals().values()))
        try:
            params = {
                'dbname': self.dbname,
                'user': self.user,
                'password': self.password,
                'host': self.host,
                'port': self.port,
                'table_name': table_name,
                'id': int(id),
            }

            res = requests.get(f'{self.URL}/delete-api', params=params)
            res = res.json()
            return res

        except:
            raise Exception(
                "There is an error with .delete() in postgres_repo.py - You may need to call .clear_cache()"
            )

    def delete_many(self, table_name: str, ids: List[int]) -> Dict[str, Any]:
        pass

    def update(
        self,
        table_name: str,
        id: int,
        updates: Dict[str, Any],
    ) -> Dict[str, Any]:
        is_args_none(args=list(locals().values()))
        try:
            # Split updates into 2 arrays
            columns_of_updates = [column for column, _ in updates.items()]
            new_values_of_updates = [value for _, value in updates.items()]
            params = {
                'dbname': self.dbname,
                'user': self.user,
                'password': self.password,
                'host': self.host,
                'port': self.port,
                'table_name': table_name,
                'id': id,
                'columns_of_updates': columns_of_updates,
                'new_values_of_updates': new_values_of_updates,
            }

            res = requests.get(f'{self.URL}/update-api', params=params)
            res: Dict[str, Any] = res.json()
            return res

        except:
            raise Exception(
                "There is an error with .update() in postgres_repo.py - You may need to call .clear_cache()"
            )

    def update_many(self):
        pass

    def find(self, table_name: str, id: int) -> Dict[str, Any]:
        pass

    def search_with_multiple_conditions(
        self,
        table_name: str,
        dto: Dict[str, Any],
    ) -> Dict[str, Any]:
        is_args_none(args=list(locals().values()))
        try:
            params = {
                'dbname': self.dbname,
                'user': self.user,
                'password': self.password,
                'host': self.host,
                'port': self.port,
                'table_name': table_name,
                'columns': list(dto.keys()),
                'values': list(dto.values()),
            }

            res = requests.get(
                f'{self.URL}/search-with-multiple-conditions-api',
                params=params,
            )
            res: List[Dict[str, Any]] = res.json()
            print(res)
            return res

        except:
            raise Exception(
                "There is an error with .search_with_multiple_conditions() in postgres_repo.py - You may need to call .clear_cache()"
            )

    def run_query(self, sql_query: str) -> List[Dict[str, Any]]:
        is_args_none(args=list(locals().values()))
        try:
            params = {
                'dbname': self.dbname,
                'user': self.user,
                'password': self.password,
                'host': self.host,
                'port': self.port,
                'sql_query': sql_query,
            }

            res = requests.get(f'{self.URL}/run-query-api', params=params)
            res: List[Dict[str, Any]] = res.json()
            return res

        except:
            raise Exception(
                "There is an error with .run_query() in postgres_repo.py - You may need to call .clear_cache()"
            )
