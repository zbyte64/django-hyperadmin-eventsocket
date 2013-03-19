from eventsocket.publishers.base import Publisher


class HyperadminLinkPublisher(Publisher):
    '''
    Submits the data to a hyperadmin link in the system
    '''
    
    def __init__(self, site, endpoint, method='POST', url_args=[], url_kwargs={}, **kwargs):
        '''
        :param site: The django url name of the site
        :param endpoint: The url name of the endpoint
        :param method: The HTTP method to use
        '''
        self.site_urlname = site
        self.endpoint_urlname = endpoint
        self.method = method.upper()
        self.url_args = url_args
        self.url_kwargs = url_kwargs
        super(HyperadminLinkPublisher, self).__init__(**kwargs)
    
    def publish(self, message):
        endpoint = self.get_endpoint()
        
        params = {
            'payload': {
                'data':message #TODO deserialize
                #ie parse_sql => MultiValueDict
            },
            'method': self.method,
            'url_args': self.url_args,
            'url_kwargs': self.url_kwargs,
        }
        #TODO this doesn't exist
        response = endpoint.internal_dispatch(**params)
        return response
    
    def get_site(self):
        pass #TODO hyperadmin.get_api(self.site_urlname)
    
    def get_endpoint(self):
        site = self.get_site()
        return site.get_endpoint_from_urlname(self.endpoint_urlname)

