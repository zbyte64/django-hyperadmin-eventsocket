from django.utils import unittest
from django import forms

from eventsocket.tests.common import StackTestCase
from eventsocket.publishers.adminlink import HyperadminLinkPublisher
from eventsocket.transformers.form import FormTransformer


class MockedItem(object):
    def __init__(self, **values):
        self.values = values
    
    def get_form(self):
        form = forms.Form(initial=self.values)
        for key, value in self.values.iteritems():
            form.fields[key] = forms.CharField()
        return form
    
    form = property(get_form)

class TestStack(StackTestCase):
    def test_simple_event(self):
        endpoint = None
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
        endpoint = None
        event = 'someevent'
        item_list = [MockedItem(name='testgroup2')]
        response = self.subscriber.notify(endpoint, event, item_list, 'uniqueid')
        self.assertEqual(response.status_code, 303)
        self.assertTrue(response.has_header('Location'))

