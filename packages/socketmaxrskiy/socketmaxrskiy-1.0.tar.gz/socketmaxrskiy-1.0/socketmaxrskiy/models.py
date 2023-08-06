import socket


class WS_Session:
    id: str
    ws_socket: socket.socket

    def __init__(self, ws_id: str, ws_socket: socket.socket):
        self.id = ws_id
        self.ws_socket = ws_socket

    def send(self, data: bytes):
        self.ws_socket.send(data)
