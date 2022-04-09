import os
import time
from typing import NoReturn
from datetime import datetime

from confluent_kafka import SerializingProducer
from confluent_kafka.schema_registry.avro import AvroSerializer
import json

from core import ccloud_config
from core.sr_api import SchemaRegistryAPI


class Producer:
    current_schema_changes = None

    def __init__(self, ccloud_config_file_path: str, model_name: str):
        self.model_name = model_name
        self._schema_registry_api = SchemaRegistryAPI(ccloud_config_file_path)
        self._current_value_schema = self._schema_registry_api.get_latest_value_schema(self.model_name)
        self._avro_serializer = AvroSerializer(
            self._schema_registry_api.get_client(),
            self._current_value_schema.schema.schema_str
        )

        conf = ccloud_config.read_ccloud_config(ccloud_config_file_path)
        producer_conf = ccloud_config.pop_schema_registry_params_from_config(conf)
        producer_conf['value.serializer'] = self._avro_serializer
        self._producer_conf = producer_conf
        self._producer = SerializingProducer(producer_conf)

    def __acked(self, err, msg) -> NoReturn:
        if err is not None:
            print("Failed to deliver message: {}".format(err))
        else:
            print("Produced record to topic {} partition [{}] @ offset {}"
                  .format(msg.topic(), msg.partition(), msg.offset()))

    def __change_configuration(self) -> NoReturn:
        self._current_value_schema = self._schema_registry_api.get_latest_value_schema(self.model_name)
        self._avro_serializer = AvroSerializer(
            self._schema_registry_api.get_client(),
            self._current_value_schema.schema.schema_str
        )
        self._producer_conf['value.serializer'] = self._avro_serializer
        self._producer = SerializingProducer(self._producer_conf)

    def change_field_name(self, old_field_name: str, new_field_name: str) -> NoReturn:
        if not self.current_schema_changes:
            current_schema = json.loads(self._current_value_schema.schema.schema_str)
        else:
            current_schema = self.current_schema_changes
        current_schema_copy = current_schema.copy()
        for idx, field in enumerate(current_schema_copy['fields']):
            if old_field_name == field['name']:
                new_item = {
                    'name': new_field_name,
                    'type': field['type']
                }
                if 'logicalType' in field:
                    new_item['logicalType'] = field['logicalType']
                current_schema['fields'].pop(idx)
                current_schema['fields'].insert(idx, new_item)
                self.current_schema_changes = current_schema
                break

    def change_field_type(self, field_name: str, old_field_type: str, new_field_type: str, new_field_logical_type: str = None) -> NoReturn:
        if not self.current_schema_changes:
            current_schema = json.loads(self._current_value_schema.schema.schema_str)
        else:
            current_schema = self.current_schema_changes
        current_schema_copy = current_schema.copy()
        for idx, field in enumerate(current_schema_copy['fields']):
            if field['name'] == field_name and field['type'] == old_field_type:
                new_item = {
                    'name': field_name,
                    'type': new_field_type
                }
                if new_field_logical_type:
                    new_item['logicalType'] = new_field_logical_type
                current_schema['fields'].pop(idx)
                current_schema['fields'].insert(idx, new_item)
                self.current_schema_changes = current_schema
                break

    def add_field(self, field_name: str, field_type: str, field_logical_type: str = None) -> NoReturn:
        if not self.current_schema_changes:
            current_schema = json.loads(self._current_value_schema.schema.schema_str)
        else:
            current_schema = self.current_schema_changes
        new_item = {
            'name': field_name,
            'type': field_type
        }
        if field_logical_type:
            new_item['logicalType'] = field_logical_type
        current_schema['fields'].append(new_item)
        self.current_schema_changes = current_schema

    def remove_field(self, field_name: str) -> NoReturn:
        if not self.current_schema_changes:
            current_schema = json.loads(self._current_value_schema.schema.schema_str)
        else:
            current_schema = self.current_schema_changes
        current_schema_copy = current_schema.copy()
        for idx, field in enumerate(current_schema_copy['fields']):
            if field_name == field['name']:
                current_schema['fields'].pop(idx)
                self.current_schema_changes = current_schema
                break

    def commit_schema_changes(self) -> NoReturn:
        if self.current_schema_changes:
            self._schema_registry_api.change_value_schema(self.model_name, json.dumps(self.current_schema_changes))
            self.__change_configuration()
            self.current_schema_changes = None

    def produce(self, value: dict, key: dict = None) -> NoReturn:
        self._producer.produce(topic=self.model_name, key=key, value=value, on_delivery=self.__acked)
        self._producer.poll(0)
        self._producer.flush()


if __name__ == '__main__':
    producer = Producer(os.getenv('CCLOUD_CONFIG_FILE_PATH'), 'shop')
    producer.produce({
        'bk': 1,
        'description': 'first description',
        'postal_code': 43009,
        'employee_count': 25
    })
    time.sleep(5)
    producer.remove_field('postal_code')
    producer.change_field_name('bk', 'pk')
    producer.change_field_type('employee_count', 'int', 'string')
    producer.add_field('date_joined', 'int', 'date')
    producer.commit_schema_changes()
    producer.produce({
        'pk': 2,
        'description': 'second description',
        'employee_count': '123',
        'date_joined': int(datetime.now().timestamp() / 60 / 60 / 24)
    })

