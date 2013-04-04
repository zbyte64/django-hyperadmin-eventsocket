from eventsocket.tests.common import StackTestCase, MockedItem, MockedEndpoint
from eventsocket.publishers.adminlink import HyperadminLinkPublisher
from eventsocket.transformers.form import FormTransformer


class TestStack(StackTestCase):
    def test_simple_event(self):
        endpoint = MockedEndpoint('this_url_name')
        event = 'someevent'
        item_list = []
        response = self.subscriber.notify(endpoint, event, item_list, 'uniqueid')
        #the default behavior is to pass back a receipt representing the message sent
        self.assertEqual(response, [])

class TestHyperadminPublishStack(StackTestCase):
    def make_publisher(self, cls=HyperadminLinkPublisher, **kwargs):
        kwargs.setdefault('site', 'hyperadmin')
        kwargs.setdefault('endpoint', 'admin_auth_group_add')
        return super(TestHyperadminPublishStack, self).make_publisher(cls, **kwargs)
    
    def make_transformer(self, cls=FormTransformer, **kwargs):
        return super(TestHyperadminPublishStack, self).make_transformer(cls, **kwargs)
    
    def test_simple_event(self):
        endpoint = MockedEndpoint('this_url_name')
        event = 'someevent'
        item_list = [MockedItem(name='testgroup2')]
        response = self.subscriber.notify(endpoint, event, item_list, 'uniqueid')
        self.assertEqual(response.status_code, 303)
        self.assertTrue(response.has_header('Location'))

