from confluent_kafka import SerializingProducer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer

from core import ccloud_config

if __name__ == '__main__':

    # Read arguments and configurations and initialize
    args = ccloud_config.parse_args()
    config_file = args.config_file
    topic = args.topic
    conf = ccloud_config.read_ccloud_config(config_file)

    # for full list of configurations, see:
    #  https://docs.confluent.io/platform/current/clients/confluent-kafka-python/#schemaregistryclient
    schema_registry_conf = {
        'url': conf['schema.registry.url'],
        'basic.auth.user.info': conf['basic.auth.user.info']}

    schema_registry_client = SchemaRegistryClient(schema_registry_conf)

    name_avro_serializer = AvroSerializer(schema_registry_client=schema_registry_client,
                                          schema_str=ccloud_config.name_schema,
                                          to_dict=ccloud_config.Name.name_to_dict)
    count_avro_serializer = AvroSerializer(schema_registry_client=schema_registry_client,
                                           schema_str=ccloud_config.count_schema,
                                           to_dict=ccloud_config.Count.count_to_dict)

    # for full list of configurations, see:
    #  https://docs.confluent.io/platform/current/clients/confluent-kafka-python/#serializingproducer
    producer_conf = ccloud_config.pop_schema_registry_params_from_config(conf)
    producer_conf['key.serializer'] = name_avro_serializer
    producer_conf['value.serializer'] = count_avro_serializer
    producer = SerializingProducer(producer_conf)

    delivered_records = 0


    # Optional per-message on_delivery handler (triggered by poll() or flush())
    # when a message has been successfully delivered or
    # permanently failed delivery (after retries).
    def acked(err, msg):
        global delivered_records
        """Delivery report handler called on
        successful or failed delivery of message
        """
        if err is not None:
            print("Failed to deliver message: {}".format(err))
        else:
            delivered_records += 1
            print("Produced record to topic {} partition [{}] @ offset {}"
                  .format(msg.topic(), msg.partition(), msg.offset()))


    for n in range(10):
        name_object = ccloud_config.Name()
        name_object.name = "alice"
        count_object = ccloud_config.Count()
        count_object.count = n
        print("Producing Avro record: {}\t{}".format(name_object.name, count_object.count))
        producer.produce(topic=topic, key=name_object, value=count_object, on_delivery=acked)
        producer.poll(0)

    producer.flush()

    print("{} messages were produced to topic {}!".format(delivered_records, topic))
