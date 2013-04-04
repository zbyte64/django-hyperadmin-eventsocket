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
    
    def publish(self, event, message):
        #id=id #CONSIDER: shouldn't messages have uuids?
        response = self.connection.index(self.index_name, event, message)
        return response
