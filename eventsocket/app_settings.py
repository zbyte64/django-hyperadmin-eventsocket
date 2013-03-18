from django.conf import settings
from django.utils.importlib import import_module

from eventsocket.loading import register_subscriber, register_publisher, register_transformer



def quick_import(path):
    path, classname = path.rsplit('.', 1)
    return getattr(import_module(path), classname)

def get_defined_task_worker():
    params = getattr(settings, 'EVENTSOCKET_WORKER', {'BACKEND':'eventsocket.tasks.PublishTasks'})
    klass = quick_import(params.pop('BACKEND'))
    return klass(**params)

def get_defined_subscibers():
    subs = getattr(settings, 'EVENTSOCKET_SUBSCRIBERS', {})
    result = dict()
    for key, sub in subs.items():
        klass = quick_import(sub.pop('BACKEND'))
        sub = register_subscriber(klass, key, sub.pop('TRANSFORMER'), sub.pop('PUBLISHER'), sub.pop('ENDPOINTS'), sub.pop('EVENTS'), sub)
        result[key] = sub
    return result

def get_defined_publishers():
    pubs = getattr(settings, 'EVENTSOCKET_PUBLISHERS', {})
    result = dict()
    for key, pub in pubs.items():
        klass = quick_import(pub.pop('BACKEND'))
        pub = register_publisher(klass, key, pub)
        result[key] = pub
    return result

def get_defined_transformers():
    trans = getattr(settings, 'EVENTSOCKET_TRANSFORMERS', {})
    result = dict()
    for key, pub in trans.items():
        klass = quick_import(pub.pop('BACKEND'))
        pub = register_transformer(klass, key, pub)
        result[key] = pub
    return result

TASK_WORKER = get_defined_task_worker()
DEFINED_SUBSCRIBERS = get_defined_subscibers()
DEFINED_PUBLISHERS = get_defined_publishers()
DEFINED_TRANSFORMERS = get_defined_transformers()

