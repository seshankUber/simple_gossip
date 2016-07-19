import sys
import socket
import time
import random
from threading import Thread


class GossipNode(object):

    infected_nodes = []

    def __init__(self, port, connection_nodes):
        self.hostname = socket.gethostname()
        self.port = port

        # socket creation
        try:
            self.node = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            print "socket created"
        except socket.error, message:
            print "Failed to create socket: {}".format(message)
            sys.exit()

        # socket binding
        try:
            self.node.bind((self.hostname, self.port))
        except socket.error, message:
            print "socket binding failed: {}".format(message)
            sys.exit()

        self.__gossip = False
        self.connection_nodes = connection_nodes

    def generate_message_and_send(self):
        while self.__gossip:
            message = input("Input message to send\n")
            self.send_message(message)

    def send_message(self, message):
        while self.connection_nodes and self.__gossip:
            receiver_address = random.choice(self.connection_nodes)
            receiver_host, receiver_port = receiver_address.split(':')
            self.node.sendto(message, (receiver_host, receiver_port))
            self.connection_nodes.remove(receiver_address)
            self.infected_nodes.append(receiver_address)

    def receive_and_forward_message(self):
        while self.__gossip:
            message_to_forward, address = self.node.recv(2048)
            sender_address = address[0] + ":" + address[1]
            self.connection_nodes.remove(sender_address)
            self.infected_nodes.append(sender_address)
            time.sleep(2)
            print "Message: {} \nReceived from {}".format(
                message_to_forward, sender_address)
            self.send_message(message_to_forward)

    def start_gossip(self, b):
        if self.__gossip:
            self.stop_gossip()
        self.__gossip = True
        t1 = Thread(target=self.receive_and_forward_message).start()
        t2 = Thread(target=self.generate_message_and_send).start()

    def stop_gossip(self):
        self.__gossip = False
