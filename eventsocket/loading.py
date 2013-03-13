
SUBSCRIBERS = dict()
PUBLISHERS = dict()
TRANSFORMERS = dict()

def register_subscriber(klass, ident, publisher, kwargs):
    '''
    Registers a subsciber
    
    :param klass: The subsciber class in instantiate
    :param ident: The key to represent the subscriber
    :param publisher: The key of the desired publisher to use
    :param kwargs: Extra params to pass to the subsciber
    '''
    params = dict(kwargs)
    params.update({
        'ident': ident,
        'publisher': publisher,
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

def register_publisher(klass, ident, transformer, kwargs):
    '''
    Registers a publisher
    
    :param klass: The publisher class in instantiate
    :param ident: The key to represent the publisher
    :param kwargs: Extra params to pass to the publisher
    '''
    params = dict(kwargs)
    params['ident'] = ident
    params.update({
        'ident': ident,
        'transformer': transformer,
    })
    pub = klass(**params)
    PUBLISHERS[ident] = pub
    return pub

def get_subscribers(endpoint, event):
    '''
    Returns a list of subscibers matching the event
    '''
    subs = list()
    for sub in SUBSCRIBERS.itervalues():
        if sub.matches_event(endpoint, event):
            subs.append(sub)
    return subs

def get_publisher(ident):
    return PUBLISHERS[ident]

def get_transformer(ident):
    return TRANSFORMERS[ident]

