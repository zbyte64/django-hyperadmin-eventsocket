import logging

from eventsocket.loading import get_publisher


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
        message = self.serialize(item_list)
        publisher = self.get_publisher()
        publisher.push(message)
    
    def serialize(self, item_list):
        '''
        Returns the serialized message
        '''
        #TODO the default should be to serialize item_list to json
        pass
    
    def get_publisher(self):
        return get_publisher(self.publisher_ident)

#other possible subscribers

class CRUDSubscriber(Subscriber):
    #would also want this split into create, update delete
    pass

#should endpoints emit a generic success event?
