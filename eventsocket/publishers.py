import logging

from eventsocket.tasks import schedule_publish


class Publisher(object):
    def __init__(self, ident, schedule=True):
        self.ident = ident
        self.schedule = schedule
    
    def get_id(self):
        return self.ident
    
    def get_logger(self):
        return logging.getLogger(__name__)
    
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
    def __init__(self, cache_name, cache_key, **kwargs):
        from django.core.cache import get_cache
        self.cache = get_cache(cache_name)
        self.cache_key = cache_key
        super(DjangoCachePublisher, self).__init__(**kwargs)
    
    def publish(self, message):
        self.cache.set(self.cache_key, message)

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

