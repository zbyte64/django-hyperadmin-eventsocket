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
    
    def push(self, message):
        '''
        Schedules the message to be sent to the publisher
        '''
        if self.schedule:
            return schedule_push(self, message)
        else:
            return self._push(message)
    
    def _push(self, message):
        message = self.transform(message)
        return self.publish(message)
    
    def transform(self, message):
        return self.get_transformer().transform(message)
    
    def publish(self, message):
        '''
        Send the mesage to the publisher
        '''
        return message

class HyperadminLinkPublisher(Publisher):
    '''
    Submits the data to a hyperadmin link in the system
    '''
    def publish(self, message):
        #get endpoint
        #get endpoint link
        #?match message to link form params?
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
    def __init__(self, channel, host='localhost', port=6379, db=0, **kwargs):
        import redis
        self.channel = channel
        self.pool = redis.ConnectionPool(host=host, port=port, db=db)
        super(RedisPublisher, self).__init__(**kwargs)
    
    def get_connection(self):
        import redis
        return redis.Redis(connection_pool=self.pool)
    
    def publish(self, message):
        connection = self.get_connection()
        connection.publish(self.channel, message)

class WebhookPublisher(Publisher):
    '''
    Publishes to a webhook
    '''
    def __init__(self, webhook_url, **kwargs):
        self.webhook_url = webhook_url
    
    def publish(self, message):
        import requests
        #CONSIDER this may want the data in form-encoded format instead of json
        response = requests.post(self.webhook_url, data=message, allow_redirects=False)

class NginxPublisher(WebhookPublisher):
    '''
    Does a post to an nginx push stream:
    https://github.com/wandenberg/nginx-push-stream-module/
    '''
    pass #how is this different from a webhook?

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

