"""
    Assigment for U5 A2: Plataforma Middleware

    Author: Eloy Uziel García Cisneros (eloy.garcia@edu.uag.mx)

    usage: from network import Network

    REF: https://www.youtube.com/watch?v=-3B1v-K1oXE&t=605s
"""


import socket
import pickle
import logging

LOGGER = logging.getLogger(__name__)

class Network:

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = "localhost" 
        self.port = 20001
        self.addr = (self.host, self.port)
        self.player_data = self.connect()

    def connect(self):
        self.client.connect(self.addr)
        data = self.client.recv(2048)
        data = pickle.loads(data)
        return data

    def send(self, data):
        try:
            data = pickle.dumps(data)
            self.client.send(data)

            reply = self.client.recv(2048)
            reply = pickle.loads(reply)
            return reply
        except socket.error as err:
            LOGGER.error('Socket error.', exc_info=True)
            raise err
        except EOFError:
            LOGGER.warning('Disconnected.')
