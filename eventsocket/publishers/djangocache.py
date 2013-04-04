from django.core.cache import get_cache

from eventsocket.publishers.base import Publisher


class DjangoCachePublisher(Publisher):
    '''
    Uses django's cache framework.
    Not meant for production.
    '''
    def __init__(self, cache_name, cache_key, **kwargs):
        
        self.cache = get_cache(cache_name)
        self.cache_key = cache_key
        super(DjangoCachePublisher, self).__init__(**kwargs)
    
    def publish(self, event, message, event_id):
        self.cache.set(self.cache_key, message)
