import unittest
import os
from typing import Dict, List, Any
from adolet_db import authenticate_db, PostgresRepo


class TestPostgresRepo(unittest.TestCase):
    '''PostgresRepo will be connected to "unittest" table in "adolet" ElephantSQL database'''
    def __init__(self, *args, **kwargs):
        super(TestPostgresRepo, self).__init__(*args, **kwargs)
        # Get database URL
        database_url: Dict[str, Any] = authenticate_db(
            email='blah@gmail.com',
            api_key=os.environ.get('ADOLET_DB_API'),
        )

        # Initialise PostgresRepo with database URL
        self.postgres_repo = PostgresRepo(
            dbname=database_url['dbname'],
            user=database_url['user'],
            password=database_url['password'],
            host=database_url['host'],
            port=int(database_url['port']),
        )

    def test_dt(self):
        '''Test .dt() of PostgresRepo'''
        tables = self.postgres_repo.dt()

        self.assertListEqual(
            tables,
            ['users_databases', 'unittest', 'users'],
        )

    def test_get_columns(self):
        '''Test that .get_columns() works and returns an array of column names of a table'''
        cols = self.postgres_repo.get_columns(table_name='unittest')

        self.assertListEqual(
            cols,
            ['id', 'name', 'age'],
        )

    def test_get_table_schema(self):
        '''Test .get_table_schema() of ClientPostgresRepo'''
        table_schema = self.postgres_repo.get_table_schema(
            table_name='unittest', )

        self.assertDictEqual(
            table_schema,
            {
                'id': 'integer',
                'name': 'text',
                'age': 'integer',
            },
        )

    def test_insert_and_delete(self):
        '''Test .insert() and .delete() of PostgresRepo'''
        dto = {'id': None, 'name': 'Tom', 'age': 20}

        inserted_dto = self.postgres_repo.insert('unittest', dto)
        deleted_dto = self.postgres_repo.delete('unittest', inserted_dto['id'])

        self.assertDictEqual(
            inserted_dto,
            deleted_dto,
        )

    def test_updgate(self):
        dto = {'id': None, 'name': 'Random Name', 'age': 100}
        inserted_dto = self.postgres_repo.insert('unittest', dto)

        updated_dto = self.postgres_repo.update(
            table_name='unittest',
            id=inserted_dto['id'],
            updates={
                'name': 'Random Name Updated',
                'age': 10,
            },
        )
        self.postgres_repo.delete('unittest', updated_dto['id'])

        # Update inserted_dto to match updated_dto
        inserted_dto['name'] = 'Random Name Updated'
        inserted_dto['age'] = 10

        self.assertDictEqual(
            inserted_dto,
            updated_dto,
        )

    def test_search_with_multiple_conditions(self):
        '''Test .search_with_multiple_conditions() of ClientPostgresRepo'''
        search_dto = {'name': 'Bob', 'age': 18}
        dto = self.postgres_repo.search_with_multiple_conditions(
            table_name='unittest',
            dto=search_dto,
        )

        self.assertDictEqual(
            dto,
            {
                'id': 1,
                'name': 'Bob',
                'age': 18,
            },
        )

    def test_run_query(self):
        '''Test .run_query() of ClientPostgresRepo'''
        dtos: List[Dict[str, Any]] = self.postgres_repo.run_query(
                sql_query="SELECT * FROM unittest WHERE id=1;", \
        )

        self.assertListEqual(
            dtos,
            [{
                'id': 1,
                'name': 'Bob',
                'age': 18
            }],
        )


if __name__ == '__main__':
    unittest.main()
