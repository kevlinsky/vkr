import os
from typing import NoReturn

from confluent_kafka.schema_registry.schema_registry_client import SchemaRegistryClient, RegisteredSchema, Schema
from core import ccloud_config
import json


class SchemaRegistryAPI:
    def __init__(self, ccloud_config_file_path):
        conf = ccloud_config.read_ccloud_config(ccloud_config_file_path)
        schema_registry_conf = {
            'url': conf['schema.registry.url'],
            'basic.auth.user.info': conf['basic.auth.user.info']
        }
        self._client = SchemaRegistryClient(schema_registry_conf)

    def get_client(self):
        return self._client

    def get_latest_key_schema(self, model_name: str) -> RegisteredSchema:
        return self._client.get_latest_version(model_name + '-key')

    def get_latest_value_schema(self, model_name: str) -> RegisteredSchema:
        return self._client.get_latest_version(model_name + '-value')

    def change_value_schema(self, model_name: str, schema: str) -> NoReturn:
        self._client.register_schema(model_name + '-value', Schema(schema, 'AVRO', []))

    def get_different_fields(self, old_schema: RegisteredSchema, new_schema: RegisteredSchema) -> dict:
        result = {
            'removed': dict(),
            'added': dict(),
            'changed': dict(),
            'links': dict()
        }

        schema1 = json.loads(old_schema.schema.schema_str)
        schema2 = json.loads(new_schema.schema.schema_str)

        s1_simple_types = dict()
        s2_simple_types = dict()
        s1_complex_types = dict()
        s2_complex_types = dict()

        for idx, field in enumerate(schema1['fields']):
            if isinstance(field['type'], str):
                if 'logicalType' in field:
                    s1_simple_types[field['name']] = field['logicalType']
                else:
                    s1_simple_types[field['name']] = field['type']
            else:
                if 'logicalType' in field['type']:
                    s1_simple_types[field['name']] = field['type']['logicalType']
                else:
                    s1_simple_types[field['name']] = field['type']['type']

                for cfield in schema1['fields'][idx]['type']['items']['fields']:
                    if schema1['fields'][idx]['name'] not in s1_complex_types:
                        s1_complex_types[schema1['fields'][idx]['name']] = dict()
                    if 'logicalType' in cfield:
                        s1_complex_types[schema1['fields'][idx]['name']][cfield['name']] = cfield['logicalType']
                    else:
                        s1_complex_types[schema1['fields'][idx]['name']][cfield['name']] = cfield['type']

        for idx, field in enumerate(schema2['fields']):
            if isinstance(field['type'], str):
                if 'logicalType' in field:
                    s2_simple_types[field['name']] = field['logicalType']
                else:
                    s2_simple_types[field['name']] = field['type']
            else:
                if 'logicalType' in field['type']:
                    s2_simple_types[field['name']] = field['type']['logicalType']
                else:
                    s2_simple_types[field['name']] = field['type']['type']

                for cfield in schema2['fields'][idx]['type']['items']['fields']:
                    if schema2['fields'][idx]['name'] not in s2_complex_types:
                        s2_complex_types[schema2['fields'][idx]['name']] = dict()
                    if 'logicalType' in cfield:
                        s2_complex_types[schema2['fields'][idx]['name']][cfield['name']] = cfield['logicalType']
                    else:
                        s2_complex_types[schema2['fields'][idx]['name']][cfield['name']] = cfield['type']

        for s in s1_simple_types:
            if s not in s2_simple_types:
                result['removed'][s] = s1_simple_types[s]

        for s in s2_simple_types:
            if s not in s1_simple_types:
                result['added'][s] = s2_simple_types[s]

        for s in s1_simple_types:
            if s in s2_simple_types:
                if s1_simple_types[s] != s2_simple_types[s]:
                    result['changed'][s] = (s1_simple_types[s], s2_simple_types[s])
                elif s1_simple_types[s] == s2_simple_types[s] == 'array':
                    result['links'][s] = {
                        'removed': dict(),
                        'added': dict(),
                        'changed': dict()
                    }
                    for ss in s1_complex_types[s]:
                        if ss not in s2_complex_types[s]:
                            result['links'][s]['removed'][ss] = s1_complex_types[s][ss]

                    for ss in s2_complex_types[s]:
                        if ss not in s1_complex_types[s]:
                            result['links'][s]['added'][ss] = s2_complex_types[s][ss]

                    for ss in s1_complex_types[s]:
                        if ss in s2_complex_types[s]:
                            if s1_complex_types[s][ss] != s2_complex_types[s][ss]:
                                result['links'][s]['changed'][ss] = (s1_simple_types[s][ss], s2_complex_types[s][ss])
                elif s1_simple_types[s] == s2_simple_types[s] == 'record':
                    pass

        return result


if __name__ == '__main__':
    api = SchemaRegistryAPI(os.getenv('CCLOUD_CONFIG_FILE_PATH'))
    receipt = api.get_latest_value_schema('receipt')
    receipt_schema = json.loads(receipt.schema.schema_str)
    print(receipt_schema)
    receipt_schema['fields'][-2]['type']['items']['fields'].append({
        'name': '123',
        'type': 'integer'
    })
    print(api.get_different_fields(receipt, RegisteredSchema(10, Schema(json.dumps(receipt_schema), 'AVRO'), 'receipt-value', 10)))
