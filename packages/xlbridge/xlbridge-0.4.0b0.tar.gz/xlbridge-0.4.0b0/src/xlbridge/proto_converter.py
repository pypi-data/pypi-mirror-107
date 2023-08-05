import logging
from . import reference_store as refstore

try:
    import numpy as np
except ImportError:
    np = None

from . import service_pb2 as proto

def convert_from_variant(v: proto.Variant):
    return proto_converter.variant(v)

def _isnumeric(x):
    obj_type = type(x)
    return obj_type==int or obj_type==float

class proto_converter:
    @classmethod
    def get_value(cls, proto_object):
        valueType = proto_object.WhichOneof('value')
        logging.debug('Converting an object of type \'%s\'', valueType)
        value = getattr(proto_object, valueType)
        func = getattr(cls, valueType)
        return func(value)

    @staticmethod
    def variant(v: proto.Variant):
        return proto_converter.get_value(v)

    @classmethod
    def matrix(cls, v: proto.VariantMatrix):
        return proto_converter.get_value(v)

    @staticmethod
    def scalar(s: proto.ScalarValue):
        global _ref_store
        value = getattr(s, s.WhichOneof('value'))
        # Since we can't really distinguish in Excel
        # between sending a string or a reference expressed
        # as a string, we need to always check if the string is
        # a valid reference
        if refstore.is_reference(value):
            logging.debug('Object is a reference')
            return refstore.get_reference(value)
        return value

    @staticmethod
    def doubleVector(dv: proto.DoubleVector):
        values = [value for value in dv.values]
        return values

    @staticmethod
    def reference(referenceAsString):
        return refstore.get_reference(referenceAsString)

    @staticmethod
    def variantMatrix(vm: proto.VariantMatrix):
        values = [proto_converter.variant(value) for value in vm.values]
        # Looping one extra time should not be needed
        if np is None or any(not _isnumeric(x) for x in values):
            mx = [values[r*vm.cols:r*vm.cols+vm.cols] for r in range(vm.rows)]
            return mx
        else:
            logging.debug('Converting an %sx%s matrix', vm.cols, vm.rows)
            arr = np.array(values)
            mx = np.reshape(arr, (vm.rows, vm.cols))
            logging.debug(mx)
            return mx

    @staticmethod
    def variantVector(vv: proto.VariantVector):
        values = [proto_converter.variant(value) for value in vv.values]
        return values

    @staticmethod
    def doubleMatrix(dm: proto.DoubleMatrix):
        values = [value for value in dm.values]
        if np is None:
            mx = [values[r*dm.cols:r*dm.cols+dm.cols] for r in range(dm.rows)]
            return mx
        mx = np.reshape(np.array(values), (dm.rows, dm.cols))
        return mx

