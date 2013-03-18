from django.utils import unittest

from eventsocket.transformers.base import Transformer
from eventsocket.publishers.base import Publisher
from eventsocket.subscribers.base import Subscriber
from eventsocket.loading import SUBSCRIBERS, PUBLISHERS, TRANSFORMERS


class TestStack(unittest.TestCase):
    def setUp(self):
        self.transformer = self.make_transformer()
        self.publisher = self.make_publisher(schedule=False)
        self.subscriber = self.make_subscriber(transformer=self.transformer, publisher=self.publisher, endpoint='.*', event='.*')
        super(TestStack, self).setUp()
    
    def make_transformer(self, cls=Transformer, **kwargs):
        kwargs.setdefault('ident', 'test-tran')
        instance = cls(**kwargs)
        TRANSFORMERS[instance.get_id()] = instance
        return instance
    
    def make_publisher(self, cls=Publisher, **kwargs):
        kwargs.setdefault('ident', 'test-pub')
        instance = cls(**kwargs)
        PUBLISHERS[instance.get_id()] = instance
        return instance
    
    def make_subscriber(self, cls=Subscriber, **kwargs):
        kwargs.setdefault('ident', 'test-sub')
        instance = cls(**kwargs)
        SUBSCRIBERS[instance.get_id()] = instance
        return instance
    
    def test_simple_event(self):
        endpoint = None
        event = 'someevent'
        item_list = []
        response = self.subscriber.notify(endpoint, event, item_list)
        #the default behavior is to pass back a receipt representing the message sent
        self.assertEqual(response, '{"items": []}')

