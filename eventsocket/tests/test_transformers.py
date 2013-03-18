from django.utils import unittest

from eventsocket.tests.common import TestCase
from eventsocket.transformers.base import Transformer
from eventsocket.transformers.singleobject import SingleObjectTransformer


class TestTransformer(TestCase):
    def setUp(self):
        super(TestTransformer, self).setUp()
        self.transformer = self.make_transformer()
    
    def test_empty_serialize(self):
        message = self.transformer.serialize([])
        self.assertEqual(message, '[]')
        
        message = self.transformer.serialize({})
        self.assertEqual(message, '{}')
    
    def test_empty_deserialize(self):
        payload = self.transformer.deserialize('[]')
        self.assertEqual(payload, [])
        
        payload = self.transformer.deserialize('{}')
        self.assertEqual(payload, {})
    
    def test_passthrough(self):
        event, message = self.transformer.transform('event', 'message')
        self.assertEqual(event, 'event')
        self.assertEqual(message, 'message')

class TestSingleObjectTransformer(TestCase):
    def setUp(self):
        super(TestSingleObjectTransformer, self).setUp()
        self.transformer = self.make_transformer(cls=SingleObjectTransformer)
    
    def test_transform(self):
        event = 'form_success'
        payload = [
            {'first_name':'John',
             'last_name':'Smith',},
            {'first_name':'Ignore',
             'last_name':'Me',}
        ]
        message = self.transformer.serialize(payload)
        r_event, r_message = self.transformer.transform(event, message)
        self.assertEqual(event, r_event)
        self.assertEqual(self.transformer.deserialize(r_message), payload[0])
    
    def test_empty_transform(self):
        event = 'form_success'
        payload = []
        message = self.transformer.serialize(payload)
        r_event, r_message = self.transformer.transform(event, message)
        self.assertEqual(event, r_event)
        self.assertEqual(r_message, '{}')

