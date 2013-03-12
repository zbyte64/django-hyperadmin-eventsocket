from django.conf import settings
from django.utils.importlib import import_module

from eventsocket.loading import register_subscriber, register_publisher



def quick_import(path):
    path, classname = path.rsplit('.', 1)
    return getattr(import_module(path), classname)

def get_defined_task_worker():
    params = getattr(SETTINGS, 'EVENTSOCKET_WORKER', {'BACKEND':'eventsocket.tasks.PublishTasks'})
    klass = quick_import(params.pop('BACKEND'))
    return klass(**params)

def get_defined_subscibers():
    subs = getattr(SETTINGS, 'EVENTSOCKET_SUBSCRIBERS', {})
    result = dict()
    for key, sub in subs.items():
        klass = quick_import(sub.pop('BACKEND'))
        sub = register_subscriber(klass, key, sub.pop('PUBLISHER'), sub)
        result[key] = sub
    return result

def get_defined_publishers():
    pubs = getattr(SETTINGS, 'EVENTSOCKET_PUBLISHERS', {})
    result = dict()
    for key, pub in subs.items():
        klass = quick_import(pub.pop('BACKEND'))
        pub = register_subscriber(klass, key, pub)
        result[key] = pub
    return result

TASK_WORKER = get_defined_task_worker()
DEFINED_SUBSCRIBERS = get_defined_subscibers()
DEFINED_PUBLISHERS = get_defined_publishers()
