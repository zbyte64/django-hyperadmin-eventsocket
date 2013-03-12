import logging
import json

from django.core.files import File

from hyperadmin.mediatypes.encoders import HyperadminJSONEncoder

from eventsocket.loading import get_publisher


#CONSIDER: is a subscriber bound to a site?
class Subscriber(object):
    def __init__(self, ident, publisher):
        self.ident = ident
        self.publisher_ident = publisher
    
    def get_id(self):
        return self.ident
    
    def get_logger(self):
        return logging.getLogger(__name__)
    
    def matches_event(self, endpoint, event):
        '''
        Return True if the subscriber should be notified of the event
        '''
        return False
    
    def notify(self, endpoint, event, item_list):
        '''
        Receives event, serializes and schedules for publishing
        '''
        message = self.serialize(endpoint, event, item_list)
        publisher = self.get_publisher()
        publisher.push(message)
    
    def serialize(self, endpoint, event, item_list):
        '''
        Returns the serialized message
        '''
        serializable_items = self.serialize_items(item_list)
        message = {
            'items': serializable_items,
            'event': event,
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

#other possible subscribers

class CRUDSubscriber(Subscriber):
    #would also want this split into create, update delete
    pass

#should endpoints emit a generic success event?
