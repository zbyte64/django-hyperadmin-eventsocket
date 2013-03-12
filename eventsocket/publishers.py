from eventsocket.tasks import schedule_publish


def get_publisher(ident):
    pass

class Publisher(object):
    schedule = True
    
    def get_id(self):
        pass
        #possibly loaded from settings
    
    def push(self, message):
        '''
        Schedules the message to be sent to the publisher
        '''
        if self.schedule:
            schedule_publish(self, message)
        else:
            self.publish(message)
        
    def publish(self, message):
        '''
        Send the mesage to the publisher
        '''
        pass

class DjangoCachePublisher(Publisher):
    '''
    Uses django's cache framework.
    Not meant for production.
    '''
    
    def publish(self, message):
        pass

#and some possible 3rd party integrations:

class RedisPublisher(Publisher):
    '''
    Uses Redis
    '''
    def publish(self, message):
        pass

class NginxPublisher(Publisher):
    '''
    Does a post to an nginx push stream:
    https://github.com/wandenberg/nginx-push-stream-module/
    '''
    
    def publish(self, message):
        pass

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

