import base64
import json
import pickle
from typing import Any

import pulsar
from _pulsar import ConsumerType, InitialPosition
from kikyo import Kikyo
from kikyo.datahub import DataHub, Producer, Consumer, Message


class PulsarBasedDataHub(DataHub):
    def __init__(self, client: Kikyo):
        settings = client.settings.deep('pulsar')
        if not settings:
            return

        self.tenant = settings.get('tenant', 'public')
        self.namespace = settings.get('namespace', 'default')
        self.pulsar = pulsar.Client(settings['service_url'])

        client.add_component('pulsar_datahub', self)

    def create_producer(self, topic: str) -> Producer:
        return PulsarBasedProducer(self, topic)

    def subscribe(self, topic: str, subscription_name: str = None, auto_ack: bool = True) -> Consumer:
        return PulsarBasedConsumer(self, topic, subscription_name=subscription_name)

    def get_topic(self, name: str):
        return f'persistent://{self.tenant}/{self.namespace}/{name}'


class PulsarBasedProducer(Producer):
    def __init__(self, datahub: PulsarBasedDataHub, topic: str):
        super().__init__()
        self.producer = datahub.pulsar.create_producer(
            datahub.get_topic(topic),
            block_if_queue_full=True,
        )

    def send(self, *records: Any):
        for record in records:
            data = MessageWrapper(record).build()
            self.producer.send_async(data, callback=self.callback)
        self.producer.flush()

    def close(self):
        self.producer.close()

    def callback(self, res, msg_id):
        pass


class PulsarMessage(Message):
    def __init__(self, msg):
        self._msg = msg
        self._value = MessageWrapper.extract_data(msg.data())

    @property
    def value(self) -> Any:
        return self._value


class PulsarBasedConsumer(Consumer):
    def __init__(
            self,
            datahub: PulsarBasedDataHub,
            topic: str, subscription_name: str = None,
            auto_ack: bool = True,
    ):
        super().__init__()
        self.consumer = datahub.pulsar.subscribe(
            datahub.get_topic(topic),
            consumer_type=ConsumerType.KeyShared,
            subscription_name=subscription_name,
            initial_position=InitialPosition.Earliest,
        )
        self._auto_ack = auto_ack

    def receive(self) -> Message:
        msg = self.consumer.receive()
        if self._auto_ack:
            self.consumer.acknowledge(msg)
        return PulsarMessage(msg)

    def close(self):
        self.consumer.close()

    def ack(self, msg: Message):
        assert isinstance(msg, PulsarMessage)
        self.consumer.acknowledge(msg._msg)


class MessageWrapper:
    ENCODING = 'utf-8'

    def __init__(self, data: Any):
        self.type = None
        self.data = None
        if isinstance(data, (dict, list)):
            self.type = 'dict'
            self.data = data
        elif isinstance(data, bytes):
            self.type = 'bytes'
            self.data = base64.b64encode(data)
        elif isinstance(data, str):
            self.type = 'str'
            self.data = data
        else:
            self.type = 'object'
            self.data = base64.b64encode(pickle.dumps(data))

    def build(self) -> bytes:
        d = {
            'type': self.type,
            'data': self.data
        }
        return json.dumps(d, ensure_ascii=False).encode(encoding=self.ENCODING)

    @classmethod
    def extract_data(cls, content: bytes) -> Any:
        message = json.loads(content.decode(encoding=cls.ENCODING))
        if message['type'] == 'dict':
            return message['data']
        if message['type'] == 'bytes':
            return base64.b64decode(message['data'])
        if message['type'] == 'str':
            return message['data']
        if message['type'] == 'object':
            return pickle.loads(base64.b64decode(message['data']))
