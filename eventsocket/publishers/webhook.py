import requests

from eventsocket.publishers.base import Publisher


class WebhookPublisher(Publisher):
    '''
    Publishes to a webhook
    '''
    def __init__(self, webhook_url, **kwargs):
        self.webhook_url = webhook_url
    
    def publish(self, event, message):
        
        #CONSIDER this may want the data in form-encoded format instead of json
        response = requests.post(self.webhook_url, data=message, allow_redirects=False)

class NginxPublisher(WebhookPublisher):
    '''
    Does a post to an nginx push stream:
    https://github.com/wandenberg/nginx-push-stream-module/
    '''
    pass #how is this different from a webhook?

