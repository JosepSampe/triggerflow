from eventprocessor_client import CloudEventProcessorClient, CloudEvent, PythonCallable
from eventprocessor_client.utils import load_config_yaml
from eventprocessor_client.sources.interfaces.kafka import KafkaCloudEventSource

if __name__ == "__main__":
    client_config = load_config_yaml('~/client_config.yaml')
    kafka_config = client_config['event_sources']['kafka']

    er = CloudEventProcessorClient(**client_config['event_processor'])

    kafka = KafkaCloudEventSource(name='my_kafka_eventsource',
                                  broker_list=kafka_config['broker_list'],
                                  topic='my_topic')

    er.create_namespace(namespace='python_callable_example',
                        global_context=client_config['global_context'],
                        event_source=kafka)

    er.target_namespace('python_callable_example')

    def my_condition(context, event):
        if 'data' in event:
            return event['data']['number'] == 123
        else:
            return False

    def my_action(context, event):
        print('Hello')

    er.add_trigger(CloudEvent('hello'),
                   condition=PythonCallable(function=my_condition),
                   action=PythonCallable(function=my_action))
