from urllib import urlencode

from django.utils import unittest

from eventsocket.tests.common import TestCase
from eventsocket.publishers.base import Publisher
from eventsocket.publishers.adminlink import HyperadminLinkPublisher


class TestPublisher(TestCase):
    def setUp(self):
        super(TestPublisher, self).setUp()
        self.publisher = self.make_publisher()
    
    def test_publish(self):
        message = self.publisher.publish('event', 'message', 'uniqueid')
        self.assertEqual(message, 'message')

class TestHyperadminLinkPublisher(TestCase):
    def setUp(self):
        super(TestHyperadminLinkPublisher, self).setUp()
        self.publisher = self.make_publisher(cls=HyperadminLinkPublisher, site='hyperadmin', endpoint='admin_auth_group_add')
    
    def test_publish(self):
        response = self.publisher.publish('event', 'name=testgroup', 'uniqueid')
        self.assertEqual(response.status_code, 303)
        self.assertTrue(response.has_header('Location'))

