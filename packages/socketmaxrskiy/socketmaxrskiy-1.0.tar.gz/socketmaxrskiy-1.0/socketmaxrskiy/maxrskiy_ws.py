import random
import socket
import string
import threading
from typing import Any, Callable

from .models import WS_Session


class WS_Server:
    on: Callable[[WS_Session, bytes], Any]
    new_connection: Callable[[WS_Session], Any]
    break_connection: Callable[[WS_Session], Any]
    all_conn: list = []
    __on = True

    def __init__(self, ip, port, on: Callable[[WS_Session, bytes], Any] = None,
                 new_connection: Callable[[WS_Session], Any] = None,
                 break_connection: Callable[[WS_Session], Any] = None):
        self.on = on
        self.new_connection = new_connection
        self.break_connection = break_connection
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((ip, port))
        server.listen(5)

        connection_handler = threading.Thread(
            target=self.handle_accept_connection,
            args=(server,)
        )
        connection_handler.start()

    def __random_word(self, length) -> str:
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for _ in range(length))

    def __check_id(self, ws_id: str) -> bool:
        all_conn_copy = self.all_conn.copy()
        for i in range(len(all_conn_copy)):
            ws_session: WS_Session = all_conn_copy[i]
            if ws_session.id == ws_id:
                return False
        return True

    def __new_id(self) -> str:
        while True:
            ws_id = self.__random_word(10)
            if not self.__check_id(ws_id):
                continue
            return ws_id

    def handle_accept_connection(self, server):
        while True:
            client_sock, address = server.accept()
            ws_session = WS_Session(self.__new_id(), client_sock)
            client_handler = threading.Thread(
                target=self.handle_client_connection,
                args=(ws_session,)
            )
            client_handler.start()

    def send(self, data: bytes):
        try:
            all_conn_copy = self.all_conn.copy()
            for i in range(len(all_conn_copy)):
                ws_session: WS_Session = all_conn_copy[i]
                ws_session.send(data)
        except OSError:
            return

    def handle_client_connection(self, ws_session: WS_Session):
        self.all_conn.append(ws_session)
        if self.new_connection is not None:
            self.new_connection(ws_session)
        while True:
            try:
                bytes_response = ws_session.ws_socket.recv(1024)
                if self.on is not None:
                    self.on(ws_session, bytes_response)
            except (ConnectionError, EOFError):
                self.__on = False
                if self.break_connection is not None:
                    self.break_connection(ws_session)
                self.all_conn.remove(ws_session)
                break
            except (KeyError):
                ws_session.send('flood_error')
                continue

    def run_until_down(self):
        while self.__on:
            pass


class WS_Client:
    server_sock: socket.socket
    on: Callable[[bytes], Any]
    break_connection: Callable[[], Any]
    __on = True

    def __init__(self, ip, port, on: Callable[[bytes], Any] = None,
                 break_connection: Callable[[], Any] = None):
        self.on = on
        self.break_connection = break_connection
        try:
            self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_sock.connect((ip, port))
            server_handler = threading.Thread(
                target=self.handle_server_connection,
            )
            server_handler.start()
        except ConnectionError:
            self.__on = False
            if self.break_connection is not None:
                self.break_connection()
            return

    def send(self, data: bytes):
        try:
            self.server_sock.send(data)
        except OSError:
            return

    def handle_server_connection(self):
        while True:
            try:
                bytes_response = self.server_sock.recv(1024)
                if self.on is not None:
                    self.on(bytes_response)
            except (ConnectionError, EOFError):
                self.__on = False
                if self.break_connection is not None:
                    self.break_connection()
                break

    def run_until_down(self):
        while self.__on:
            pass
