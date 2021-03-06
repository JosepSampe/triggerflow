# TriggerFlow: Event-based Orchestration of Serverless Workflows

Triggerflow is a scalable, extensible and serverless in design platform for event-based orchestration of
serverless workflows.

![triggerflow_architecture](https://user-images.githubusercontent.com/33722759/85291482-d46b8180-b49a-11ea-973f-3995b21425ad.png)

Triggerflow follows an Event-Condition-Action architecture with stateful triggers that can aggregate, filter,
process and route incoming events from a variety of event sources in a consistent and fault tolerant way.

Thanks to Triggerflow's extensibility provided by its fully programmable trigger condition and action functions, and 
combining and chaining multiple triggers, we can orchestrate different serverless workflow abstractions such as
DAGs (Apache Airflow), State Machines (Amazon Step Functions), and Workflow as Code like (Azure Durable Functions),
among other specialized workflows.

Triggerflow has been implemented using Open-Source Cloud Native projects like CloudEvents and KEDA or Knative.
When Triggerflow is deployed using KEDA or Knative, the trigger processing service runs only when there are incoming
events so that it can be scaled down to zero when it is not used, which results in a pay-per-use serverless model.

You can read more about Triggerflow architecture and features in the
[Triggerflow: Trigger-based Orchestration of Serverless Workflows](https://arxiv.org/abs/2006.08654) article, presented 
and accepted at the [ACM Distributed and Event Based Systems 2020 conference](https://2020.debs.org/accepted-papers/).

## Documentation

### Installation and deployment
- [Triggerflow Client Installation](docs/CLIENT_INSTALL.md)

- [Standalone Deployment for testing guide](deploy/standalone/README.md)

- [Knative on Kubernetes Deployment guide](deploy/knative/README.md)

- [KEDA on Kubernetes Deployment guide](deploy/keda/README.md)

### Examples
- [DAG Interface example](examples/dag-example/count_words.ipynb)

- [ASL State Machines example](docs/STATEMACHINES.md)

- [Workflow As Code example](docs/WORKFLOWASCODE.md)

- [Triggerflow Experiments instructions for replication](docs/EXPERIMENTS.md)

## Triggerflow Client Example
```python
from triggerflow import Triggerflow, CloudEvent, DefaultConditions
from triggerflow.functions import PythonCallable
from triggerflow.eventsources.rabbit import RabbitMQEventSource

# Instantiate Triggerflow client
tf_client = Triggerflow()

# Create a workspace and add a RabbitMQ event source to it
rabbitmq_source = RabbitMQEventSource(amqp_url='amqp://guest:guest@172.17.0.3/', queue='My-Queue')
tf_client.create_workspace(workspace_name='test', event_source=rabbitmq_source)


def my_action(context, event):
    context['message'] += 'World!'

# Create the trigger activation event 
activation_event = CloudEvent().SetEventType('test.event.type').SetSubject('Test')

# Create a trigger with a custom Python callable action and a Join condition that joins 10 events
tf_client.add_trigger(trigger_id='MyTrigger',
                      event=activation_event,
                      condition=DefaultConditions.JOIN,
                      action=PythonCallable(my_action),
                      context={'message': 'Hello ', 'join': 10})

# Publish 10 activation events, the action will only be executed on the 10th event
for _ in range(10):
    rabbitmq_source.publish_cloudevent(activation_event)

# Retrieve the trigger's context
trg = tf_client.get_trigger('MyTrigger')
print(trg['context']['message'])  # Prints 'Hello World!'
```   
