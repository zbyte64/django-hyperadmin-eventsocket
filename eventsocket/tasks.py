from eventsocket.loading import get_publisher


def schedule_push(publisher, message):
    from eventsocket.app_settings import TASK_WORKER
    TASK_WORKER.schedule_push(publisher, message)

def execute_push(ident, message):
    '''
    The actual function to be executed by the task to publish the message
    
    :param ident: The id of the publisher
    '''
    publisher = get_publisher(ident)
    publisher._push(message)

class PublishTasks(object):
    def schedule_push(self, publisher, message):
        schedule_push(publisher.get_id(), message)

class ZTaskPublishTasks(PublishTasks):
    def __init__(self):
        super(ZTaskPublishTasks, self).__init__()
        from django_ztask.decorators import task
        self._schedule_push = task()(schedule_push)
    
    def schedule_push(self, publisher, message):
        self._schedule_push.async(ident=publisher.get_id(), message=message)

class CeleryPublishTasks(PublishTasks):
    def __init__(self):
        super(CeleryPublishTasks, self).__init__()
        from celery.task import task
        self._schedule_push = task(schedule_push, ignore_result=True)
    
    def schedule_push(self, publisher, message):
        self.schedule_push.delay(ident=publisher.get_id(), message=message)
