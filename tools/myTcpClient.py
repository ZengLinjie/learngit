#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from tornado import ioloop, httpclient, gen
import pdb, time, logging
import tornado.ioloop
import tornado.iostream
import socket

class MyTCPClient(object):
    def __init__(self, host, port, io_loop=None):
        self.host = host
        self.port = port
        self.io_loop = io_loop

        self.shutdown = False
        self.stream = None
        self.sock_fd = None

        self.EOF = b' END'


    def get_stream(self):
        self.sock_fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        self.stream = tornado.iostream.IOStream(self.sock_fd)
        self.stream.set_close_callback(self.on_close)

    def connect(self):
        self.get_stream()
        self.stream.connect((self.host, self.port), self.send_message)

    def on_receive(self, data):
        logging.info("Received: %s", data)
        self.stream.close()

    def on_close(self):
        if self.shutdown:
            self.io_loop.stop()

    def send_message(self):
        self.stream.write(b"Hello Server!" + self.EOF)
        self.stream.read_until(self.EOF, self.on_receive)

    def set_shutdown(self):
        self.shutdown = True