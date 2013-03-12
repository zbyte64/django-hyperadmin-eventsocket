from eventsocket.loading import get_publisher


def schedule_publish(publisher, message):
    from eventsocket.app_settings import TASK_WORKER
    TASK_WORKER.schdule_publish(publisher, message)

def execute_publish(ident, message):
    '''
    The actual function to be executed by the task to publish the message
    
    :param ident: The id of the publisher
    '''
    publisher = get_publisher(ident)
    publisher.publish(message)

class PublishTasks(object):
    def schedule_publish(self, publisher, message):
        execute_publish(publisher.get_id(), message)

class ZTaskPublishTasks(PublishTasks):
    def __init__(self):
        super(ZTaskPublishTasks, self).__init__()
        from django_ztask.decorators import task
        self._execute_publish = task()(execute_publish)
    
    def schedule_publish(self, publisher, message):
        self._execute_publish.async(ident=publisher.get_id(), message=message)

class CeleryPublishTasks(PublishTasks):
    def __init__(self):
        super(CeleryPublishTasks, self).__init__()
        from celery.task import task
        self._execute_publish = task(execute_publish, ignore_result=True)
    
    def schedule_publish(self, publisher, message):
        self._execute_publish.delay(ident=publisher.get_id(), message=message)
