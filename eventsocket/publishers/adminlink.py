from urlparse import parse_qsl

from django.utils.datastructures import MultiValueDict

from hyperadmin import get_api

from eventsocket.publishers.base import Publisher


class HyperadminLinkPublisher(Publisher):
    '''
    Submits the data to a hyperadmin link in the system
    '''
    
    def __init__(self, site, endpoint, method='POST', url_args=[], url_kwargs={}, **kwargs):
        '''
        :param site: The django namespace of the site
        :param endpoint: The url name of the endpoint
        :param method: The HTTP method to use
        '''
        self.site_namespace = site
        self.endpoint_urlname = endpoint
        self.method = method.upper()
        self.url_args = url_args
        self.url_kwargs = url_kwargs
        super(HyperadminLinkPublisher, self).__init__(**kwargs)
    
    def publish(self, event, message, event_id):
        endpoint = self.get_endpoint()
        
        data = MultiValueDict(parse_qsl(message))
        params = {
            'payload': {
                'data':data
                #CONSIDER: how do we support files?
            },
            'method': self.method,
            'url_args': self.url_args,
            'url_kwargs': self.url_kwargs,
        }
        response = endpoint.internal_dispatch(**params)
        return response
    
    def get_site(self):
        return get_api(self.site_namespace)
    
    def get_endpoint(self):
        site = self.get_site()
        return site.get_endpoint_from_urlname(self.endpoint_urlname)

