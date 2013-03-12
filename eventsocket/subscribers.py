def get_subscribers(endpoint, event):
    '''
    Returns a list of subscibers matching the event
    '''
    return []

class Subscriber(object):
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
        pass

#other possible subscribers

class CRUDSubscriber(Subscriber):
    #would also want this split into create, update delete
    pass

#should endpoints emit a generic success event?
