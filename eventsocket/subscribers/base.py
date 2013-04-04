import logging
import re
import io

from django import forms

from datatap.datataps import JSONDataTap

from eventsocket.loading import get_publisher, get_transformer


#these might make life easier:
#hyperadmin.forms.ResourceItemField(resource=urlname?) => text field
#hyperadmin.forms.ResourceItemChoiceField(resource=urlname?) => choice field
#hyperadmin.forms.ResourceItemMultiChoiceField(resource=urlname?) => multi choice field
#should endpoints emit a generic success event?

class SubscriberConfigForm(forms.Form):
    ident_suffix = forms.SlugField('ident') #ident = virtual-<ident_suffix>
    transformer = forms.SlugField() #ident of transformer
    publisher = forms.SlugField(help_text='The ident of the publisher') #CONSIDER: reference publisher resource
    endpoints = forms.SlugField() #needs to be a list that you can select; a bit overwhelming, need rawid
    #Hyperadmin introspection resource?
    #find: endpoints, resources, etc
    #all available endpoints as items; does not directly link since some need url kwargs
    #publishers resource, r/o for settings defined, the rest editable and addable
    events = forms.CharField() #ideally gives choices based on endpoints
#perhaps only one endpoint and one event
#workflow:
# select subscriber type
# select endpoint
# select event
# select publisher
# ? transformer

#CONSIDER: is a subscriber bound to a site?
class Subscriber(object):
    def __init__(self, ident, transformer, publisher, endpoint, event):
        self.ident = ident
        
        #we pass around idents to the task worker
        if hasattr(transformer, 'get_id'):
            transformer = transformer.get_id()
        if hasattr(publisher, 'get_id'):
            publisher = publisher.get_id()
        self.transformer_ident = transformer
        self.publisher_ident = publisher
        self.endpoint = re.compile(endpoint)
        self.event = re.compile(event)
    
    def get_id(self):
        return self.ident
    
    def get_logger(self):
        return logging.getLogger(__name__)
    
    def matches_endpoint(self, endpoint):
        return bool(self.endpoint.match(endpoint.get_url_name()))
    
    def matches_event(self, event):
        '''
        Return True if the subscriber should be notified of the event
        '''
        return bool(self.event.match(event))
    
    def notify(self, endpoint, event, item_list, event_id):
        '''
        Receives event, serializes and schedules for publishing
        
        :param endpoint: A hyperadmin endpoint bound to an api request
        :param event: A string representing the event
        :param item_list: A list of hypermedia items
        :param event_id: A unique identifier representing the originating event
        '''
        message = self.serialize(endpoint, event, item_list)
        publisher = self.get_publisher()
        transformer = self.get_transformer()
        return publisher.push(transformer, event, message, event_id)
    
    def serialize(self, endpoint, event, item_list):
        '''
        Returns the serialized message
        '''
        datatap = endpoint.get_datatap(instream=item_list)
        serialized_dt = JSONDataTap(instream=datatap)
        payload = io.BytesIO()
        serialized_dt.send(payload)
        return payload.getvalue()
    
    def get_publisher(self):
        return get_publisher(self.publisher_ident)
    
    def get_transformer(self):
        return get_transformer(self.transformer_ident)
    
    def __repr__(self):
        return '<{cls}:{ident} event:{event}, endpoint:{endpoint}, publisher:{publisher}, transformer:{transformer}>'.format(
            cls=type(self),
            ident=self.ident,
            event=self.event.pattern,
            endpoint=self.endpoint.pattern,
            publisher=self.publisher_ident,
            transformer=self.transformer_ident,
        )

