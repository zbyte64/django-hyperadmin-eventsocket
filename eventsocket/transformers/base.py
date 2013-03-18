import logging
import json

from hyperadmin.mediatypes.encoders import HyperadminJSONEncoder


class Transformer(object):
    def __init__(self, ident):
        self.ident = ident
    
    def get_id(self):
        return self.ident
    
    def get_logger(self):
        return logging.getLogger(__name__)
    
    def serialize(self, payload):
        '''
        Serializes primitive python data types for use by the publisher and transformer
        '''
        return json.dumps(payload, cls=HyperadminJSONEncoder)
    
    def deserialize(self, message):
        '''
        Deserializes a message into primitive python data types
        '''
        return json.loads(message)
    
    def transform(self, event, message):
        '''
        Returns a tuple of the modified event and message
        '''
        return self.transform_event(event), self.transform_message(message)
    
    def transform_event(self, event):
        return event
    
    def transform_message(self, message):
        return message

