#! /usr/bin/env python
# coding=utf-8
import traceback

import tornado
from tornado.iostream import StreamClosedError
from tornado.tcpserver import TCPServer

from tools.utils import Utils

TCP_MAX_LENGTH = 1024


class TCPConnection(object):

     def __init__(self, stream, address):
        self._stream = stream
        self._address = address
        self.read_message()

     @tornado.gen.coroutine
     def read_message(self):
        try:
          r =  self._stream.read_bytes(TCP_MAX_LENGTH, partial=True)
          data = yield r
          self.broadcast_messages(data)
        except Exception as e:
                if isinstance(e,StreamClosedError):
                    self.on_close()
                else:
                    msg = traceback.format_exc()  # 方式1
                    Utils().logMainDebug(msg)

     def broadcast_messages(self, data):
        self.send_message(data)
        # print("User said:", data[:-1], self._address)
        # for conn in Connection.clients:
        #     conn.send_message(data)
        self.read_message()

     def send_message(self, data):
        self._stream.write(data)

     def on_close(self):
        print("A user has left the chat room.", self._address)
        TCPConnection.clients.remove(self)


class ChatServer(TCPServer):
    def handle_stream(self, stream, address):
        print("New connection :", address, stream)
        TCPConnection(stream, address)
        print("connection num is:", len(Connection.clients))

