import logging


class Transformer(object):
    def __init__(self, ident):
        self.ident = ident
    
    def get_id(self):
        return self.ident
    
    def get_logger(self):
        return logging.getLogger(__name__)
    
    def transform(self, message):
        '''
        Returns a modified message
        '''
        return message

