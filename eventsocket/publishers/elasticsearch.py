from pyelasticsearch import ElasticSearch

from eventsocket.publishers.base import Publisher


class ElasticSearchPublisher(Publisher):
    '''
    Publishes to an ElasticSearch Index
    '''
    def __init__(self, elasticsearch_url, index_name, **kwargs):
        self.elasticsearch_url = elasticsearch_url
        self.index_name = index_name
        self.connection = ElasticSearch(self.elasticsearch_url)
    
    def publish(self, event, message, event_id):
        response = self.connection.index(self.index_name, event, message, id=event_id)
        return response
