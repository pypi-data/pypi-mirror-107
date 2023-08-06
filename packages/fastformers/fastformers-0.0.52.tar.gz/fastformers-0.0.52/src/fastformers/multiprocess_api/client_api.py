from typing import List, Dict

import time
import select
import socket
import threading
import uuid
import pickle

from ..utils import logger
from .socket_connection import SocketConnection
from .configs import Config


class ClientSocket(SocketConnection):
    def __init__(self, connection: socket.socket, message_size: int):
        super().__init__(connection, message_size)
        self.connection.setblocking(False)

    def empty(self):
        self.connection.recv(self.message_size)

    def request_server(self):
        self.connection.send(Config.request_signal)

    def cancel_request(self):
        self.connection.send(Config.request_cancelled)


class ClientAPI:
    client_sockets: Dict[bytes, Dict[str, List[ClientSocket]]] = {}

    def __init__(self, model: str, model_config):
        self.model = model
        self.model_config = model_config

    @staticmethod
    def create_sockets(model, model_config, attempts: int, wait_time: float) -> List[ClientSocket]:
        logger.debug('Connecting to model workers')
        model_sockets: List[ClientSocket] = []
        for worker_ind in range(len(model_config.allocations)):
            client_socket = socket.socket()
            for _ in range(attempts):
                try:
                    client_socket.connect((Config.host, model_config.port + worker_ind))
                    logger.debug(f'{model} model worker {worker_ind} connected')
                    model_sockets.append(
                        ClientSocket(connection=client_socket, message_size=Config.client_message_size))
                    break
                except ConnectionRefusedError:
                    time.sleep(wait_time)
        return model_sockets

    def forward(self, **inputs):
        thread_id = threading.get_ident().to_bytes(length=Config.message_id_len - 16, byteorder='big', signed=False)

        if thread_id not in self.client_sockets:
            self.client_sockets[thread_id] = {}
        if self.model not in self.client_sockets[thread_id]:
            self.client_sockets[thread_id][self.model] = self.create_sockets(
                self.model, self.model_config, attempts=120, wait_time=10)
        client_sockets = self.client_sockets[thread_id][self.model]

        buffered_sockets = select.select(client_sockets, [], [], 0)[0]

        for client_socket in buffered_sockets:
            client_socket.empty()

        for client_socket in client_sockets:
            client_socket.request_server()

        selected_socket: ClientSocket = select.select(client_sockets, [], [], None)[0][0]

        for client_socket in client_sockets:
            if client_socket.fileno() != selected_socket.fileno():
                client_socket.cancel_request()

        selected_socket.empty()

        message_id = thread_id + uuid.uuid4().bytes

        selected_socket.send_message(message_id, inputs)

        selected_socket.connection.setblocking(True)
        while True:
            data = selected_socket.read_buffer()
            response_message_id = data[:Config.message_id_len]
            if response_message_id == message_id:
                break
            response_thread_id = response_message_id[:-16]
            if response_thread_id != thread_id:
                logger.error(f'Worker {thread_id} received message with worker id {response_thread_id}')
            else:
                logger.warning(
                    f'Skipping response with id {response_message_id} on worker {thread_id}, target id is {message_id}')
        selected_socket.connection.setblocking(False)
        data = data[Config.message_id_len:]

        if data.startswith(Config.error_prefix):
            raise ConnectionError(data[len(Config.error_prefix):].decode('utf-8'))

        return pickle.loads(data)

    def __call__(self, **kwargs):
        return self.forward(**kwargs)

    def close(self):
        for client_sockets in self.client_sockets.values():
            for sockets in client_sockets.values():
                for client_socket in sockets:
                    client_socket.close()
