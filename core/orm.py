from typing import Any, List, NoReturn

import psycopg2
import os


class Database:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Database, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self._connection = psycopg2.connect(
            host=os.getenv('POSTGRES_HOST'),
            port=os.getenv('POSTGRES_PORT'),
            database=os.getenv('POSTGRES_DB_NAME'),
            user=os.getenv('POSTGRES_USER'),
            password=os.getenv('POSTGRES_PASSWORD')
        )
        self._cursor = self._connection.cursor()

        self.avro_to_db_types = {
            'integer': 'integer',
            'string': 'character varying',
            'boolean': 'boolean',
            'float': 'double precision',
            'date': 'date'
        }

    def get_all_hubs(self) -> List[Any]:
        db_name = os.getenv('POSTGRES_DB_NAME')
        query = f'SELECT table_name FROM {db_name}.information_schema.tables where lower(table_name) like \'hub_%\''
        self._cursor.execute(query)
        return [item[0] for item in self._cursor.fetchall()]

    def get_all_satellites(self) -> List[Any]:
        db_name = os.getenv('POSTGRES_DB_NAME')
        query = f'SELECT table_name FROM {db_name}.information_schema.tables where lower(table_name) like \'satellite_%\''
        self._cursor.execute(query)
        return [item[0] for item in self._cursor.fetchall()]

    def get_all_links(self) -> List[Any]:
        db_name = os.getenv('POSTGRES_DB_NAME')
        query = f'SELECT table_name FROM {db_name}.information_schema.tables where lower(table_name) like \'link_%\''
        self._cursor.execute(query)
        return [item[0] for item in self._cursor.fetchall()]

    def get_model_satellites(self, model_name: str) -> List[Any]:
        db_name = os.getenv('POSTGRES_DB_NAME')
        query = f'SELECT table_name FROM {db_name}.information_schema.tables where lower(table_name) like \'satellite_{model_name}%\''
        self._cursor.execute(query)
        return [item[0] for item in self._cursor.fetchall()]

    def get_model_links(self, model_name: str) -> List[Any]:
        db_name = os.getenv('POSTGRES_DB_NAME')
        query = f'SELECT table_name FROM {db_name}.information_schema.tables where lower(table_name) like \'link_%\''
        self._cursor.execute(query)
        result = self._cursor.fetchall()
        r = list()
        for row in result:
            if model_name in row[0]:
                r.append(row[0])
        return r

    def get_model_fields(self, model_name: str) -> dict[str, List[str]]:
        result = dict()
        db_name = os.getenv('POSTGRES_DB_NAME')
        satellites = self.get_model_satellites(model_name)
        for satellite in satellites:
            query = f'SELECT column_name, data_type FROM {db_name}.information_schema.columns where table_name = \'{satellite}\''
            self._cursor.execute(query)
            columns = self._cursor.fetchall()
            result[satellite] = columns
        return result

    def add_field(self, model_name: str, field_name: str, field_type: str) -> NoReturn:
        query = f'ALTER TABLE satellite_{model_name} ADD COLUMN {field_name} {self.avro_to_db_types[field_type]}'
        self._cursor.execute(query)
        self._connection.commit()

    def remove_field(self, model_name: str, field_name: str, field_type: str) -> NoReturn:
        model_fields = self.get_model_fields(model_name)
        for satellite, columns in model_fields.items():
            for column in columns:
                if column[0] == field_name and column[1] == self.avro_to_db_types[field_type]:
                    query = f'ALTER TABLE {satellite} DROP COLUMN {column[0]}'
                    self._cursor.execute(query)
        self._connection.commit()

    def create_new_satellite(self, model_name: str) -> str:
        model_satellites = self.get_model_satellites(model_name)
        table_name = f'satellite_{model_name}_{len(model_satellites)}'
        query = f'CREATE TABLE {table_name} (' \
                f'{model_name}_id INTEGER NOT NULL CONSTRAINT {table_name}_hub_{model_name}_id_fk' \
                f'REFERENCES hub_{model_name}' \
                f'from_date DATE NOT NULL' \
                f'to_date DATE' \
                f')'
        self._cursor.execute(query)
        self._connection.commit()
        return table_name

    def change_field_type(self, model_name: str, field_name: str, new_field_type: str):
        satellite_name = self.create_new_satellite(model_name)
        query = f'ALTER TABLE {satellite_name} ADD COLUMN {field_name} {self.avro_to_db_types[new_field_type]}'
        self._cursor.execute(query)
        self._connection.commit()
