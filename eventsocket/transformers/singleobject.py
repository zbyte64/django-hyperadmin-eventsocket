from eventsocket.transformers.base import Transformer


class SingleObjectMixin(object):
    '''
    A mixin that converts the message to represent a single item
    '''
    def deserialize(self, message):
        data = super(SingleObjectMixin, self).deserialize(message)
        if len(data):
            data = data[0]
        else:
            data = {}
        return data

class SingleObjectTransformer(SingleObjectMixin, Transformer):
    '''
    Converts the message to represent a single item
    '''
    pass

