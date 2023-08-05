import logging
import inspect
import asyncio
import time
from concurrent import futures
from grpc import aio

from . import service_pb2_grpc
from .xlbridge_servicer import XlBridgeServicer

def server(address = '[::]:47074'):
    return ExcelBridgeServer(address)

class ExcelBridgeServer:
    def __init__(self, address = '[::]:47074'):
        self._functions = []
        self._address = address

    async def serve(self):
        server = aio.server(futures.ThreadPoolExecutor(max_workers=10))
        servicer = XlBridgeServicer(self._functions)
        service_pb2_grpc.add_BridgeServiceServicer_to_server(servicer, server)
        print(f'Starting server. Listening on {self._address}.')
        server.add_insecure_port(self._address)
        await server.start()
        await server.wait_for_termination()

    def run(self):
        asyncio.run(self.serve())

    def add(self, obj):
        if inspect.ismodule(obj):
            self._functions.extend(func for name, func in inspect.getmembers(obj, inspect.isfunction) if not name.startswith('_'))
        elif inspect.isfunction(obj):
            self._functions.append(obj)
        

