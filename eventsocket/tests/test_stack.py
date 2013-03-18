from django.utils import unittest

from eventsocket.tests.common import StackTestCase


class TestStack(StackTestCase):
    def test_simple_event(self):
        endpoint = None
        event = 'someevent'
        item_list = []
        response = self.subscriber.notify(endpoint, event, item_list)
        #the default behavior is to pass back a receipt representing the message sent
        self.assertEqual(response, '{"items": []}')

