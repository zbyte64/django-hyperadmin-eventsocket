
def schedule_publish(publisher, message):
    #foward to celery or ztask
    publisher.get_id() #for later lookup
    pass


def execute_publish(ident, message):
    '''
    The actual function to be executed by the task to publish the message
    
    :param ident: The id of the publisher
    '''
    from eventsocket.publishers import get_publisher
    publisher = get_publisher(ident)
    publisher.publish(message)

