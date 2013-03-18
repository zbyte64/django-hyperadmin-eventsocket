
SUBSCRIBERS = dict()
PUBLISHERS = dict()
TRANSFORMERS = dict()

def register_subscriber(klass, ident, transformer, publisher, endpoints, events, kwargs):
    '''
    Registers a subsciber
    
    :param klass: The subsciber class in instantiate
    :param ident: The key to represent the subscriber
    :param transformer: The key of the desired transformer to use
    :param publisher: The key of the desired publisher to use
    :param endpoints: A list url url names matching the endpoint to listen to
    :param events: A list of events to listen to
    :param kwargs: Extra params to pass to the subsciber
    '''
    params = dict(kwargs)
    params.update({
        'ident': ident,
        'transformer': transformer,
        'publisher': publisher,
        'endpoints': endpoints,
        'events': events,
    })
    sub = klass(**params)
    SUBSCRIBERS[ident] = sub
    return sub

def register_transformer(klass, ident, kwargs):
    '''
    Registers a transformer
    
    :param klass: The transformer class in instantiate
    :param ident: The key to represent the transformer
    :param kwargs: Extra params to pass to the transformer
    '''
    params = dict(kwargs)
    params['ident'] = ident
    tran = klass(**params)
    TRANSFORMERS[ident] = tran
    return tran

def register_publisher(klass, ident, kwargs):
    '''
    Registers a publisher
    
    :param klass: The publisher class in instantiate
    :param ident: The key to represent the publisher
    :param kwargs: Extra params to pass to the publisher
    '''
    params = dict(kwargs)
    params['ident'] = ident
    pub = klass(**params)
    PUBLISHERS[ident] = pub
    return pub

def get_subscribers(endpoint, event):
    '''
    Returns a list of subscibers matching the event
    '''
    subs = list()
    for sub in SUBSCRIBERS.itervalues():
        if sub.matches_endpoint(endpoint) and sub.matches_event(event):
            subs.append(sub)
    return subs

def get_publisher(ident):
    return PUBLISHERS[ident]

def get_transformer(ident):
    return TRANSFORMERS[ident]

