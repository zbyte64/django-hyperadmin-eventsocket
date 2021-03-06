from eventsocket.tests.common import StackTestCase, MockedEndpoint
from eventsocket.loading import SUBSCRIBERS, get_subscribers


class TestSubscriber(StackTestCase):
    def setUp(self):
        super(TestSubscriber, self).setUp()
        self.selective_subscriber = self.make_subscriber(transformer=self.transformer, publisher=self.publisher, endpoint='^another_url', event='^someotherevent$', ident='test-selectivesub')
    
    def test_empty_serialize(self):
        endpoint = MockedEndpoint('this_url_name')
        event = 'someevent'
        item_list = []
        message = self.subscriber.serialize(endpoint, event, item_list)
        self.assertEqual(message, '[]')
    
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

