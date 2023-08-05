import logging
import asyncio
from types import FunctionType
import inspect

from .proto_converter import convert_from_variant
from .object_converter import convert_to_variant, custom_error_as_variant
from .reference_store import dispose_reference

from .service_pb2 import FunctionList, FunctionDef, ArgumentDef, ArgumentMode, TypeDef, PrimitiveDef, DisposeReferenceResult, StatusResponse, ConnectionStatus
from .service_pb2_grpc import BridgeServiceServicer

class XlBridgeServicer(BridgeServiceServicer):
    _functions = {}

    def __init__(self, functions):
        self._functions = { func.__name__ : func for func in functions }

    async def Call(self, request, context):
        logging.debug('Remote call \'%s\' with parameters \'%s\'', request.name, str(request.parameters).replace('\n', ''))
        args = [convert_from_variant(arg)
            for arg in request.parameters]
        func = self._functions[request.name]
        try:
            if inspect.iscoroutinefunction(func):
                res = await _call_expanded_async(func, args)
            else:
                res = _call_expanded(func, args)
            return convert_to_variant(res)
        except Exception as exp:
            return custom_error_as_variant(exp)
        except:
            return custom_error_as_variant("Exception")

    async def Subscribe(self, request, context):
        logging.debug('Remote subscription \'%s\' with parameters \'%s\'', request.name, str(request.parameters).replace('\n', ''))
        args = [convert_from_variant(arg)
            for arg in request.parameters]
        func = self._functions[request.name]
        async for res in _call_expanded(func, args):
            yield convert_to_variant(res)

    async def SubscribeToStatus(self, request, context):
        resp = StatusResponse()
        resp.status = ConnectionStatus.Alive
        async for val in _delayed_sequence(resp, 10):
            yield val

    def DisposeReference(self, request, context):
        dispose_reference(request.reference)
        return DisposeReferenceResult()

    def GetFunctionList(self, request, context):
        fl = FunctionList()
        fl.functions.extend(_get_proto_functions(self._functions))
        return fl

def _get_proto_functions(functions):
    return [_get_proto_function(func, signature) for func, signature
        in [(func, _get_signature(func)) for func in functions.values()]
        if signature is not inspect.Signature.empty]

async def _delayed_sequence(val, delay):
    while True:
        yield val
        await asyncio.sleep(delay)

_type_to_net_type = {
    int: 'int',
    str: 'string',
    float: 'double',
    bool: 'bool',
    object: 'object'
}

def _get_signature(func):
    try:
        sig = inspect.signature(func)
    except:
        sig = inspect.Signature.empty
    return sig

def _get_proto_function(py_func, sig):
    logging.debug('Found function %s(%s)', py_func.__name__, ', '.join(p for p in sig.parameters))

    proto_func = FunctionDef()
    proto_func.name = py_func.__name__
    proto_func.description = py_func.__name__
    proto_func.category = 'pybridge'
    proto_func.isHidden = False
    proto_func.isVolatile = False

    returnType = proto_func.returnType
    returnType.isNullable = True
    if inspect.iscoroutinefunction(py_func):
        returnType.mode = ArgumentMode.ArgumentModeAsync
    elif inspect.isasyncgenfunction(py_func):
        returnType.mode = ArgumentMode.ArgumentModeStream
    else:
        returnType.mode = ArgumentMode.ArgumentModeSync
    returnType.type = _type_to_net_type[object]
    returnType.primitiveValue.SetInParent()

    params = sig.parameters
    args = [_get_proto_argument(name, params[name])
            for name in params]
    proto_func.arguments.extend(args)
    return proto_func


def _get_proto_argument(name, param):
    proto_arg = ArgumentDef()
    proto_arg.name = name
    proto_arg.description = name

    type_def = proto_arg.type

    if param.kind == inspect.Parameter.VAR_POSITIONAL:
        proto_arg.isParams = True
        # Hack to hard-code .NET type here
        type_def.type = 'object[]'
    else:
        proto_arg.isParams = False
        type_def.type = _type_to_net_type[object]

    return proto_arg

def _call_expanded(func, args):
    logging.debug('Calling \'%s\' with \'%s\'', func.__name__, args)
    params = inspect.signature(func).parameters
    expanded = []
    for name, arg in zip(params, args):
        param = params[name]
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            expanded.extend(arg)
        else:
            expanded.append(arg)
    logging.debug(expanded)
    return func(*expanded)

async def _call_expanded_async(func, args):
    logging.debug('Asynchronously calling \'%s\' with \'%s\'', func.__name__, args)
    return await _call_expanded(func, args)

