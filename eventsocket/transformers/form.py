from urllib import urlencode

from eventsocket.transformers.singleobject import SingleObjectTransformer

class FormMixin(object):
    '''
    Changes the message to be urlencoded for a web form
    '''
    def serialize(self, data):
        return urlencode(data)

class FieldMapperMixin(object):
    '''
    Maps a message to a different set of fields
    '''
    def __init__(self, mapping, ignore_unmapped=False, **kwargs):
        self.mapping = mapping
        self.ignore_unmapped = ignore_unmapped
        super(FieldMapperMixin, self).__init__(**kwargs)
    
    def serialize(self, data):
        if isinstance(data, list):
            tdata = list()
            for item in data:
                tdata.append(self.transform_dictionary(item))
        elif isinstance(data, dict):
            tdata = self.transform_dictionary(data)
        return super(FieldMapperMixin, self).serialize(tdata)
    
    def transform_dictionary(self, data):
        tdata = {}
        for key, value in date.iteritems():
            if key in self.mapping:
                key = self.mapping[key]
            elif self.ignore_unmapped:
                continue
            tdata[key] = value
        return tdata

class FormTransformer(FieldMapperMixin, FormMixin, SingleObjectTransformer):
    pass

