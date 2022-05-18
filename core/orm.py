import json
from datetime import date
from typing import Any, List, NoReturn, Optional, Dict
import re

import psycopg2
import os


class Database:
    def __new__(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = super(Database, cls).__new__(cls)
        return cls._instance

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
            'int': 'integer',
            'string': 'character varying',
            'boolean': 'boolean',
            'float': 'double precision',
            'date': 'date'
        }

        self.db_to_avro_types = {
            'integer': 'int',
            'character varying': 'string',
            'boolean': 'boolean',
            'double precision': 'float',
            'date': 'date'
        }

        self.binary_avro_types = ['int', 'string', 'float', 'boolean']
        self.complex_avro_types = ['date']

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
        result = [item[0] for item in self._cursor.fetchall()]
        return sorted(result)

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

    def get_model_fields(self, model_name: str) -> Dict[str, List[str]]:
        result = dict()
        db_name = os.getenv('POSTGRES_DB_NAME')
        satellites = self.get_model_satellites(model_name)
        for satellite in satellites:
            query = f'SELECT column_name, data_type FROM {db_name}.information_schema.columns where table_name = \'{satellite}\''
            self._cursor.execute(query)
            columns = self._cursor.fetchall()
            result[satellite] = columns
        return result

    def delete_link(self, model_name: str, linked_model_name: str) -> NoReturn:
        links = self.get_model_links(model_name)
        for link in links:
            if model_name in link and linked_model_name in link:
                query = f'DROP TABLE {link}'
                self._cursor.execute(query)
                self._connection.commit()
                break

    def create_link(self, model_name: str, linked_model_name: str) -> NoReturn:
        hubs = self.get_all_hubs()
        if linked_model_name in hubs:
            query = f'CREATE TABLE link_{linked_model_name}_{model_name}(' \
                    f'{linked_model_name}_id integer not null ' \
                    f'constraint link_{linked_model_name}_{model_name}_hub_{linked_model_name}_id_fk ' \
                    f'references hub_{linked_model_name},' \
                    f'{model_name}_id integer not null ' \
                    f'constraint link_{linked_model_name}_{model_name}_hub_{model_name}_id_fk ' \
                    f'references hub_{model_name},' \
                    'from_date date not_null,' \
                    'to_date date' \
                    ')'
            self._cursor.execute(query)
            self._connection.commit()

    def create_satellite(self, model_name: str) -> str:
        model_satellites = self.get_model_satellites(model_name)
        table_name = f'satellite_{model_name}_{len(model_satellites)}'
        query = f'CREATE TABLE {table_name} (' \
                f'{model_name}_id INTEGER NOT NULL CONSTRAINT {table_name}_hub_{model_name}_id_fk ' \
                f'REFERENCES hub_{model_name}, ' \
                f'from_date DATE NOT NULL, ' \
                f'to_date DATE' \
                f')'
        self._cursor.execute(query)
        self._connection.commit()
        return table_name

    def field_exist(self, field_name: str, table_name: str) -> bool:
        db_name = os.getenv('POSTGRES_DB_NAME')
        query = f'SELECT column_name, data_type FROM {db_name}.information_schema.columns where table_name = \'{table_name}\''
        self._cursor.execute(query)
        columns = self._cursor.fetchall()
        exist = False
        for column in columns:
            if column[0] == field_name:
                exist = True
                break
        return exist

    def add_field(self, model_name: str, field_name: str, field_type: str, satellite: str = None) -> NoReturn:
        if '_id' in field_name:
            linked_model_name = re.sub('_id', '', field_name)
            self.create_link(model_name, linked_model_name)
        elif field_name != 'bk' and not self.field_exist(field_name, satellite):
            if satellite:
                query = f'ALTER TABLE {satellite} ADD COLUMN {field_name} {self.avro_to_db_types[field_type]}'
            else:
                query = f'ALTER TABLE satellite_{model_name} ADD COLUMN {field_name} {self.avro_to_db_types[field_type]}'
            self._cursor.execute(query)
            self._connection.commit()

    def remove_field(self, model_name: str, field_name: str, field_type: str) -> NoReturn:
        if '_id' in field_name:
            linked_model_name = re.sub('_id', '', field_name)
            self.delete_link(model_name, linked_model_name)
        elif field_name != 'bk':
            model_fields = self.get_model_fields(model_name)
            for satellite, columns in model_fields.items():
                for column in columns:
                    if column[0] == field_name and column[1] == self.avro_to_db_types[field_type]:
                        query = f'ALTER TABLE {satellite} DROP COLUMN {column[0]}'
                        self._cursor.execute(query)
                        self._connection.commit()
                        break

    def get_field_satellite(self, model_name: str, field_name: str, field_type: str) -> Optional[str]:
        for satellite, fields in self.get_model_fields(model_name).items():
            for field in fields:
                if field[0] == field_name and field[1] == self.avro_to_db_types[field_type]:
                    return satellite
        return None

    def change_field_type(self, model_name: str, field_name: str, old_field_type: str, new_field_type: str) -> NoReturn:
        if field_name == 'bk':
            return

        old_field_satellite = self.get_field_satellite(model_name, field_name, old_field_type)
        model_satellites = self.get_model_satellites(model_name)
        satellite_idx = model_satellites.index(old_field_satellite)
        if satellite_idx == len(model_satellites) - 1:
            satellite_name = self.create_satellite(model_name)
            for field in self.get_model_fields(model_name)[model_satellites[-1]]:
                if field[0] == field_name:
                    self.add_field(model_name, field[0], new_field_type, satellite_name)
                else:
                    self.add_field(model_name, field[0], self.db_to_avro_types[field[1]], satellite_name)
        else:
            self.add_field(model_name, field_name, new_field_type, model_satellites[satellite_idx + 1])

    def get_model_id(self, model_name: str, bk: int) -> int:
        query = f'SELECT id FROM hub_{model_name} WHERE bk = {bk}'
        self._cursor.execute(query)
        idx = self._cursor.fetchone()
        return int(idx[0])

    def put_link_data(self, model_name: str, model_idx: int, linked_model_name: str, value: Any) -> NoReturn:
        existing_links = self.get_model_links(model_name)
        target_link = None
        for link in existing_links:
            if model_name in link and linked_model_name in link:
                target_link = link
                break

        if target_link:
            query = f'UPDATE {target_link} SET to_date = %s WHERE {model_name}_id = %s ' \
                    f'AND {linked_model_name}_id = %s AND to_date IS NULL'
            self._cursor.execute(query, (date.today(), model_idx, value))
            self._connection.commit()

            query = f'INSERT INTO {target_link} ({model_name}_id, {linked_model_name}_id, from_date, to_date) VALUES' \
                    f'(%s, %s, %s, %s)'
            self._cursor.execute(query, (model_idx, value, date.today(), None))
            self._connection.commit()

    def put_satellite_data(self, model_idx: int, model_name: str, satellite_name: str, data: dict) -> NoReturn:
        for model_satellite in self.get_model_satellites(model_name):
            query = f'UPDATE {model_satellite} SET to_date = %s WHERE {model_name}_id = %s ' \
                    f'AND to_date IS NULL'
            self._cursor.execute(query, (date.today(), model_idx))
        self._connection.commit()

        fields = ', '.join(data.keys())
        values = ', '.join(['%s' for _ in data.values()])
        query = f'INSERT INTO {satellite_name} ({model_name}_id, {fields}, from_date, to_date) VALUES (%s, {values}, %s, %s)'
        values_list = [model_idx, ]
        values_list += list(data.values())
        values_list.append(date.today())
        values_list.append(None)
        self._cursor.execute(query, tuple(values_list))
        self._connection.commit()

    def put_hub_data(self, model_name: str, bk: int) -> NoReturn:
        query = f'SELECT COUNT(1) FROM hub_{model_name} WHERE bk = {bk}'
        self._cursor.execute(query)
        count = self._cursor.fetchone()[0]
        if not count:
            query = f'INSERT INTO hub_{model_name} (bk, from_date, to_date) VALUES (%s, %s, %s)'
            self._cursor.execute(query, (bk, date.today(), None))
            self._connection.commit()

    def put_model_data(self, model_name: str, data: dict, latest_value_schema: str) -> NoReturn:
        schema_fields = json.loads(latest_value_schema)['fields']
        fields_types = dict()
        for field in schema_fields:
            if 'logicalType' in field:
                fields_types[field['name']] = field['logicalType']
            else:
                fields_types[field['name']] = field['type']
        bk = data.pop('bk', None)
        if not bk:
            return
        self.put_hub_data(model_name, bk)
        idx = self.get_model_id(model_name, bk)

        satellite_data = dict()
        satellite_name = self.get_model_satellites(model_name)[-1]
        for key, value in data.items():
            if '_id' in key:
                linked_model_name = re.sub('_id', '', key)
                self.put_link_data(model_name, idx, linked_model_name, value)
            else:
                if fields_types[key] == 'date':
                    value = date.fromtimestamp(float(value) * 24 * 60 * 60)
                    satellite_data[key] = value
                elif fields_types[key] in self.binary_avro_types:
                    satellite_data[key] = value

        self.put_satellite_data(idx, model_name, satellite_name, satellite_data)


if __name__ == '__main__':
    db = Database()
    print(db.get_model_id('customer', 1))
