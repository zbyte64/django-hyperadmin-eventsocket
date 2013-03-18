from django.utils import unittest

from eventsocket.tests.common import StackTestCase
from eventsocket.loading import SUBSCRIBERS, get_subscribers


class MockedEndpoint(object):
    def __init__(self, url_name):
        self.url_name = url_name
    
    def get_url_name(self):
        return self.url_name

class TestSubscriber(StackTestCase):
    def setUp(self):
        super(TestSubscriber, self).setUp()
        self.selective_subscriber = self.make_subscriber(transformer=self.transformer, publisher=self.publisher, endpoint='^another_url', event='^someotherevent$', ident='test-selectivesub')
    
    def test_empty_serialize(self):
        endpoint = None
        event = 'someevent'
        item_list = []
        message = self.subscriber.serialize(endpoint, event, item_list)
        self.assertEqual(message, '{"items": []}')
    
    def test_matches_endpoint(self):
        endpoint = MockedEndpoint('this_url_name')
        self.assertTrue(self.subscriber.matches_endpoint(endpoint))
        
        self.assertFalse(self.selective_subscriber.matches_endpoint(endpoint))
    
    def test_matches_event(self):
        self.assertTrue(self.subscriber.matches_event('someevent'))
        
        self.assertFalse(self.selective_subscriber.matches_event('someevent'))
    
    def test_get_subscribers(self):
        assert SUBSCRIBERS, str(SUBSCRIBERS)
        
        endpoint = MockedEndpoint('this_url_name')
        event = 'someevent'
        results = get_subscribers(endpoint, event)
        
        self.assertEqual(len(results), 1)
        
        endpoint = MockedEndpoint('another_url')
        event = 'someotherevent'
        results = get_subscribers(endpoint, event)
        
        self.assertEqual(len(results), 2)

