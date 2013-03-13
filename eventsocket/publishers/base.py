import logging

from eventsocket.tasks import schedule_push
from eventsocket.loading import get_transformer


class Publisher(object):
    def __init__(self, ident, transformer, schedule=True):
        self.ident = ident
        self.schedule = schedule
        self.transformer_ident = transformer
    
    def get_id(self):
        return self.ident
    
    def get_logger(self):
        return logging.getLogger(__name__)
    
    def get_transformer(self):
        return get_transformer(self.transformer_ident)
    
    def push(self, event, message):
        '''
        Schedules the message to be sent to the publisher
        '''
        if self.schedule:
            return schedule_push(self, event, message)
        else:
            return self._push(event, message)
    
    def _push(self, event, message):
        event, message = self.transform(event, message)
        return self.publish(event, message)
    
    def transform(self, event, message):
        return self.get_transformer().transform(event, message)
    
    def publish(self, event, message):
        '''
        Send the mesage to the publisher
        '''
        return message



#and some possible 3rd party integrations:
"""
class PubnubPublisher(Publisher):
    '''
    Does a push to Pubnub:
    http://www.pubnub.com/
    '''

    def publish(self, message):
        pass

class PusherPublisher(Publisher):
    '''
    Does a push to Pusher:
    http://pusher.com/
    '''
    
    def publish(self, message):
        pass

class ElasticSearchPublisher(Publisher):
    '''
    Publishes items to elastic search index
    '''
    
    def publish(self, message):
        pass
"""

