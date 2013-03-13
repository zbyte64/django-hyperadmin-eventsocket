import redis

from eventsocket.publishers.base import Publisher


class RedisPublisher(Publisher):
    '''
    Puplish to redis
    '''
    def __init__(self, channel, host='localhost', port=6379, db=0, **kwargs):
        self.channel = channel
        self.pool = redis.ConnectionPool(host=host, port=port, db=db)
        super(RedisPublisher, self).__init__(**kwargs)
    
    def get_connection(self):
        return redis.Redis(connection_pool=self.pool)
    
    def publish(self, event, message):
        connection = self.get_connection()
        connection.publish(self.channel, message)
