import os
from typing import NoReturn

from confluent_kafka import DeserializingConsumer, Message
from confluent_kafka.error import ValueDeserializationError
from confluent_kafka.schema_registry import RegisteredSchema
from confluent_kafka.schema_registry.avro import AvroDeserializer

from core import ccloud_config
from core.orm import Database
from core.sr_api import SchemaRegistryAPI


class Consumer:
    def __init__(self, ccloud_config_file_path: str, model_name: str):
        self.model_name = model_name
        self._schema_registry_api = SchemaRegistryAPI(ccloud_config_file_path)
        self._current_value_schema = self._schema_registry_api.get_latest_value_schema(model_name)
        self._avro_deserializer = AvroDeserializer(
            self._schema_registry_api.get_client(),
            self._current_value_schema.schema.schema_str
        )

        conf = ccloud_config.read_ccloud_config(ccloud_config_file_path)
        consumer_conf = ccloud_config.pop_schema_registry_params_from_config(conf)
        consumer_conf['group.id'] = 'dwh_group'
        consumer_conf['value.deserializer'] = self._avro_deserializer
        consumer_conf['auto.offset.reset'] = 'earliest'
        self._consumer_conf = consumer_conf
        self._consumer = DeserializingConsumer(consumer_conf)
        self._consumer.subscribe([model_name,])
        self._db = Database()

    def __change_configuration(self, new_schema: RegisteredSchema) -> NoReturn:
        self._current_value_schema = new_schema
        self._avro_deserializer = AvroDeserializer(
            self._schema_registry_api.get_client(),
            self._current_value_schema.schema.schema_str
        )
        self._consumer_conf['value.deserializer'] = self._avro_deserializer
        self._consumer = DeserializingConsumer(self._consumer_conf)
        self._consumer.subscribe([self.model_name,])

    def consume(self) -> NoReturn:
        while True:
            try:
                msg = self._consumer.poll(1.0)
                if msg is None:
                    print("Waiting for message or event/error in poll()")
                    continue
                elif msg.error():
                    print(f'Error occurred: {msg.error()}')
                else:
                    model_name = msg.key()
                    model_value = msg.value()
                    print(f"Consumed record with key {model_name} and value {model_value}")
            except KeyboardInterrupt:
                break
            except ValueDeserializationError as e:
                print("Message deserialization failed. Trying to change the schema")
                new_schema = self._schema_registry_api.get_latest_value_schema(self.model_name)
                changes = self._schema_registry_api.get_different_fields(self._current_value_schema, new_schema)
                for field_name, field_type in changes['removed'].items():
                    self._db.remove_field(self.model_name, field_name, field_type)
                for field_name, field_type in changes['added'].items():
                    self._db.add_field(self.model_name, field_name, field_type)
                for field_name, (old_field_type, new_field_type) in changes['changed'].items():
                    self._db.change_field_type(self.model_name, field_name, old_field_type, new_field_type)
                self._consumer.close()
                self.__change_configuration(new_schema)
                print(f'Schema changed for message - {e.kafka_message.value()}')
                self._consumer.poll(1.0)

        self._consumer.close()


if __name__ == '__main__':
    consumer = Consumer(os.getenv('CCLOUD_CONFIG_FILE_PATH'), 'shop')
    consumer.consume()
