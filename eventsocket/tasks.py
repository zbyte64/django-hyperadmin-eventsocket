from eventsocket.loading import get_publisher, get_transformer


def schedule_push(transformer, publisher, event, message, event_id):
    from eventsocket.app_settings import TASK_WORKER
    return TASK_WORKER.schedule_push(transformer.get_ident(), publisher.get_ident(), event, message, event_id)

def execute_push(transformer_ident, publisher_ident, event, message, event_id):
    '''
    The actual function to be executed by the task to publish the message
    
    :param ident: The id of the publisher
    '''
    transformer = get_transformer(transformer_ident)
    publisher = get_publisher(publisher_ident)
    event, message = transformer.transform(event, message)
    return publisher._push(event, message, event_id)

class PublishTasks(object):
    def schedule_push(self, transformer_ident, publisher_ident, event, message, event_id):
        return execute_push(transformer_ident, publisher_ident, event, message, event_id)

class ZTaskPublishTasks(PublishTasks):
    def __init__(self):
        super(ZTaskPublishTasks, self).__init__()
        from django_ztask.decorators import task
        self._execute_push = task()(execute_push)
    
    def schedule_push(self, transformer_ident, publisher_ident, event, message, event_id):
        return self._execute_push.async(transformer_ident=transformer_ident, publisher_ident=publisher_ident, event=event, message=message, event_id=event_id)

class CeleryPublishTasks(PublishTasks):
    def __init__(self):
        super(CeleryPublishTasks, self).__init__()
        from celery.task import task
        self._execute_push = task(execute_push, ignore_result=True)
    
    def schedule_push(self, transformer_ident, publisher_ident, event, message, event_id):
        return self._execute_push.delay(transformer_ident=transformer_ident, publisher_ident=publisher_ident, event=event, message=message, event_id=event_id)

