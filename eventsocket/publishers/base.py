import logging

from eventsocket.tasks import schedule_push, execute_push


class Publisher(object):
    def __init__(self, ident, schedule=True):
        self.ident = ident
        self.schedule = schedule
    
    def get_id(self):
        return self.ident
    
    def get_logger(self):
        return logging.getLogger(__name__)
    
    def push(self, transformer, event, message, event_id):
        '''
        Schedules the message to be sent to the publisher
        '''
        if self.schedule:
            return schedule_push(transformer, self, event, message, event_id)
        else:
            return execute_push(transformer.get_id(), self.get_id(), event, message, event_id)
    
    def _push(self, event, message, event_id):
        return self.publish(event, message, event_id)
    
    def publish(self, event, message, event_id):
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

