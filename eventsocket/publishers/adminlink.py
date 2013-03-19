from eventsocket.publishers.base import Publisher

class HyperadminLinkPublisher(Publisher):
    '''
    Submits the data to a hyperadmin link in the system
    '''
    
    def __init__(self, site, endpoint, method='POST', **kwargs):
        '''
        :param site: The django url name of the site
        :param endpoint: The url name of the endpoint
        :param method: The HTTP method to use
        '''
        self.site = site
        self.endpoint = endpoint
        self.method = method
        super(HyperadminLinkPublisher, self).__init__(**kwargs)
    
    def publish(self, message):
        #get endpoint
        #get endpoint link
        #?match message to link form params?
        pass

