import logging

_ref_index = 0
_ref_store = {}

def dispose_reference(referenceAsString):
    global _ref_store
    try:
        del _ref_store[referenceAsString]
        logging.info('Disposed reference \'%s\'', referenceAsString)
    except KeyError:
        logging.warn('Reference \'%s\' not found when disposing', referenceAsString)
        pass

def is_reference(value):
    global _ref_store
    return type(value)==str and value.startswith('eb:') and value in _ref_store

def add_reference(obj):
    global _ref_store, _ref_index
    # This should probably be made thread-safe, but so should
    # a lot of other stuff
    _ref_index += 1
    idx = _ref_index
    name = f"eb:{type(obj).__name__}:{idx}"
    _ref_store[name] = obj
    logging.info('Added reference \'%s\'', name)
    return name

def get_reference(value):
    global _ref_store
    try:
        obj = _ref_store[value]
        logging.debug('Accessed reference \'%s\'', value)
        return obj
    except:
        logging.warn('Could not access reference \'%s\'', value)
        pass
