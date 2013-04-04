import requests

from eventsocket.publishers.base import Publisher


class WebhookPublisher(Publisher):
    '''
    Publishes to a webhook
    '''
    def __init__(self, webhook_url, method='POST', **kwargs):
        self.webhook_url = webhook_url
        self.method = method
    
    def publish(self, event, message, event_id):
        action = getattr(requests, self.method.lower())
        response = action(self.webhook_url, data=message, allow_redirects=False)
        return response

class NginxPublisher(WebhookPublisher):
    '''
    Does a post to an nginx push stream:
    https://github.com/wandenberg/nginx-push-stream-module/
    '''
    pass #how is this different from a webhook?

