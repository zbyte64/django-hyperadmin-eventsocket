import uuid

from hyperadmin.signals import endpoint_event, resource_event

from eventsocket.loading import get_subscribers


@endpoint_event.connect
def publish_endpoint_event(endpoint, event, item_list, **kwargs):
    '''
    Pushes the endpoint event to the matching registered subscribers
    '''
    subscribers = get_subscribers(endpoint, event)
    if subscribers:
        event_id = uuid.uuid1()
        for subscriber in subscribers:
            subscriber.notify(endpoint, event, item_list, event_id=event_id)

@resource_event.connect
def publish_resource_event(resource, event, item_list, **kwargs):
    '''
    Pushes the resource event to the matching registered subscribers
    '''
    subscribers = get_subscribers(resource, event)
    if subscribers:
        event_id = uuid.uuid1()
        for subscriber in subscribers:
            subscriber.notify(resource, event, item_list, event_id=event_id)
