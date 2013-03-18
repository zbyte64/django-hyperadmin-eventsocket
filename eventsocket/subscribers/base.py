import logging
import json
import re

from django.core.files import File
from django import forms

from hyperadmin.mediatypes.encoders import HyperadminJSONEncoder

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
    
    def notify(self, endpoint, event, item_list):
        '''
        Receives event, serializes and schedules for publishing
        '''
        message = self.serialize(endpoint, event, item_list)
        publisher = self.get_publisher()
        transformer = self.get_transformer()
        return publisher.push(transformer, event, message)
    
    def serialize(self, endpoint, event, item_list):
        '''
        Returns the serialized message
        '''
        serializable_items = self.serialize_items(item_list)
        message = {
            'items': serializable_items,
        }
        return json.dumps(message, cls=HyperadminJSONEncoder)
    
    def serialize_items(self, item_list):
        serializable_items = list()
        for item in item_list:
            serializable_items.append(self.serialize_item(item))
        return serializable_items
    
    #CONSIDER this is redundant in mediatype. Should factor this out
    def serialize_item(self, item):
        return self.get_form_instance_values(item.form)
    
    def prepare_field_value(self, val):
        if isinstance(val, File):
            if hasattr(val, 'name'):
                val = val.name
            else:
                val = None
        return val
    
    def get_form_instance_values(self, form):
        data = dict()
        for name, field in form.fields.iteritems():
            val = form[name].value()
            val = self.prepare_field_value(val)
            data[name] = val
        return data
    
    def get_publisher(self):
        return get_publisher(self.publisher_ident)
    
    def get_transformer(self):
        return get_transformer(self.transformer_ident)

