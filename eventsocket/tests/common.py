from django.utils import unittest

from eventsocket.transformers.base import Transformer
from eventsocket.publishers.base import Publisher
from eventsocket.subscribers.base import Subscriber
from eventsocket.loading import SUBSCRIBERS, PUBLISHERS, TRANSFORMERS


class TestCase(unittest.TestCase):
    '''
    A test case with helper methods for use with eventsocket
    '''
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

class StackTestCase(TestCase):
    '''
    A test case meant for testing an entire event
    '''
    def setUp(self):
        self.transformer = self.make_transformer()
        self.publisher = self.make_publisher(schedule=False)
        self.subscriber = self.make_subscriber(transformer=self.transformer, publisher=self.publisher, endpoint='.*', event='.*')
        super(StackTestCase, self).setUp()

