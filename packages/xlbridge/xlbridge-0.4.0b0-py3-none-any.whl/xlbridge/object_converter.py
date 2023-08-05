import logging
from . import reference_store as refstore

try:
    import numpy as np
except ImportError:
    np = None

from . import service_pb2 as proto

def convert_to_variant(obj):
    logging.debug('Converting to variant: %s', obj)
    if obj is None:
        return _error_variant(proto.ErrorType.ErrorTypeNull)
    elif isinstance(obj, list):
        return _list_to_variant(obj)
    elif np is not None and isinstance(obj, np.ndarray):
        return _ndarray_to_variant(obj)
    elif isinstance(obj, tuple):
        return _list_to_variant(list(obj))
    elif _isscalar(obj):
        return _scalar_variant(obj)
    else:
        # If we didn't recognize the type until we got here
        # it has to be returned as a reference
        return _reference_variant(obj)

def custom_error_as_variant(msg):
    v = proto.Variant()
    error = v.scalar.errorValue
    if type(msg)==None:
        error.type = proto.ErrorType.ErrorTypeNull
    elif type(msg)==ZeroDivisionError:
        error.type = proto.ErrorType.ErrorTypeDiv0
    elif type(msg)==Exception:
        error.type = proto.ErrorType.ErrorTypeUnknown
        error.name = type(msg).__name__
        error.message = type(msg).__name__
    elif type(msg)==str:
        error.type = proto.ErrorType.ErrorTypeUnknown
        error.name = msg
        error.message = msg
    else:
        error.type = proto.ErrorType.ErrorTypeUnknown
    return v

_type_to_proto_name = {
    str: 'stringValue',
    int: 'intValue',
    float: 'doubleValue',
    bool: 'boolValue'
}

def _isnumeric(x):
    obj_type = type(x)
    return obj_type==int or obj_type==float

def _isscalar(x):
    obj_type = type(x)
    return obj_type in _type_to_proto_name

def _check_list_type(obj: list):
    if all(_isnumeric(item) for item in obj):
        return "numeric"
    elif all(_isscalar(item) for item in obj):
        return "scalar"
    elif all(isinstance(item, list) for item in obj):
        return "lists"
    else:
        return "invalid"

def _double_matrix_variant(rows: int, cols: int, values):
    v = proto.Variant()
    matrix = v.matrix
    dm = matrix.doubleMatrix
    dm.rows = rows
    dm.cols = cols
    dm.values.extend(values)
    return v

def _double_vector_variant(values):
    v = proto.Variant()
    matrix = v.matrix
    dv = matrix.doubleVector
    dv.values.extend(values)
    return v

def _variant_vector_variant(values):
    v = proto.Variant()
    matrix = v.matrix
    dv = matrix.variantVector
    dv.values.extend(convert_to_variant(item) for item in values)
    return v


def _variant_matrix_variant(rows: int, cols: int, values):
    v = proto.Variant()
    matrix = v.matrix
    dm = matrix.variantMatrix
    dm.rows = rows
    dm.cols = cols
    dm.values.extend(convert_to_variant(item) for item in values)
    return v

def _scalar_variant(obj):
    v = proto.Variant()
    s = v.scalar
    setattr(s, _type_to_proto_name[type(obj)], obj)
    return v

def _error_variant(errorType: proto.ErrorType):
    v = proto.Variant()
    error = v.scalar.errorValue
    error.type = errorType
    return v

def _reference_variant(obj):
    v = proto.Variant()
    v.reference = refstore.add_reference(obj)
    return v

def _ndarray_to_variant(obj):
    v = proto.Variant()
    if obj.ndim==0:
        return _scalar_variant(obj.tolist())
    elif obj.ndim==1:
        return _double_vector_variant(obj.tolist())
    elif obj.ndim==2:
        return _double_matrix_variant(obj.shape[0], obj.shape[1], obj.flat)

def _list_to_variant(obj: list):
    res = _check_list_type(obj)
    if res=="numeric":
        return _double_vector_variant(obj)
    elif res=="scalar":
        return _variant_vector_variant(obj)
    elif res=="lists":
        return _list_of_lists_to_matrix(obj)
    else:
        return custom_error_as_variant("items must be numeric or scalar")

def _list_of_lists_to_matrix(obj: list):
    rows = len(obj)
    cols_per_row = [len(row) for row in obj]
    cols = max(cols_per_row)
    if all(x==cols for x in cols_per_row):
        flattened = [item for row in obj for item in row]
        res = _check_list_type(flattened)
        if res=="numeric":
            return _double_matrix_variant(rows, cols, flattened)
        elif res=="scalar":
            return _variant_matrix_variant(rows, cols, flattened)
        else:
            return custom_error_as_variant("items must be numeric or scalar")
    else:
        return custom_error_as_variant("rows must be of equal length")
