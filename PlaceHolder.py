class PlaceHolder:
    '''
    This class is a place holder that is supposed to return when opening a 
    file is failed.

    This is such that when we call close on all supposedly opened file descriptors (some may not even be because the open() failed), it won't 
    raise any error.
    '''

    _main_object = None
    
    def __init__(self):
        return

    def close(self):
        return

    def __eq__(self, other: 'PlaceHolder'):

        if (isinstance(other, PlaceHolder)):
            return True

        return False

    @classmethod
    def get_place_holder(cls):

        if (cls._main_object == None):
            cls._main_object = PlaceHolder()

        return cls._main_object
