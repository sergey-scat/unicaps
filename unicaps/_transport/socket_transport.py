# -*- coding: UTF-8 -*-
"""
Transport and requests for socket protocol
"""

import errno
import json
import random
import select
import socket
from typing import Optional, Dict

from .base import BaseTransport, BaseRequest  # type: ignore
from ..exceptions import NetworkError, ServiceError  # type: ignore


class StandardSocketTransport(BaseTransport):
    """ Standard socket Transport """

    SOCKET_HOST = None
    SOCKET_PORTS = None
    LINE_TERMINATOR = b'\r\n'

    def __init__(self, settings: Optional[Dict] = None):
        super().__init__(settings)
        self._socket = None

    def _sendrecv(self, data):
        fds = [self._socket]
        buf = bytes(data, 'utf-8') + self.LINE_TERMINATOR
        response = bytes()
        # intvl_idx = 0
        while True:
            intvl = 1  # , intvl_idx = self._get_poll_interval(intvl_idx)
            rds, wrs, exs = select.select(
                (not buf and fds) or [], (buf and fds) or [], fds, intvl
            )
            if exs:
                raise NetworkError('select() failed')
            try:
                if wrs:
                    while buf:
                        buf = buf[wrs[0].send(buf):]
                elif rds:
                    while True:
                        part_of_response = rds[0].recv(256)
                        if not part_of_response:
                            raise NetworkError('recv(): connection lost')
                        response += part_of_response
            except socket.error as err:
                if (err.errno not in
                        (errno.EAGAIN, errno.EWOULDBLOCK, errno.EINPROGRESS)):
                    raise NetworkError('Socket error') from err
            if response.endswith(self.LINE_TERMINATOR):
                # self._log('RECV', response)
                return str(response.rstrip(self.LINE_TERMINATOR), 'utf-8')
        raise ServiceError('send/recv timed out')

    def _make_request(self, request_data: Dict) -> Dict:
        if not self._socket:
            self.connect()
        return self._sendrecv(request_data)

    def connect(self):
        """ Establishes connection with service """

        host = (socket.gethostbyname(self.SOCKET_HOST),
                random.choice(self.SOCKET_PORTS))

        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.settimeout(0)
        try:
            self._socket.connect(host)
        except socket.error as err:
            if (err.errno not in
                    (errno.EAGAIN, errno.EWOULDBLOCK, errno.EINPROGRESS)):
                self.close()
                raise

        return self._socket

    def close(self):
        """ Close the connection """

        if self._socket:
            # self._log('CLOSE')
            try:
                self._socket.shutdown(socket.SHUT_RDWR)
            except socket.error:
                pass
            finally:
                self._socket.close()
                self._socket = None

    def __del__(self):
        """ Close the connection on object delete """

        self.close()


class SocketRequestJSON(BaseRequest):
    """ HTTP Request that returns JSON response """

    def parse_response(self, response) -> Dict:  # pylint: disable=no-self-use
        """ Parse response """

        try:
            return json.loads(response)
        except json.decoder.JSONDecodeError:
            raise ServiceError("Unable to parse respponse from the server: bad JSON")
