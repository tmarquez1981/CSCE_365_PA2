import sys
import socket
import random

import Checksum
import pickle

'''
This is the basic sender class. Your sender will extend this class and will
implement the start() method.
'''
class BasicSender(object):
    def __init__(self,dest,port,filename,debug=False):
        self.debug = debug
        self.dest = dest
        self.dport = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(None) # blocking
        self.sock.bind(('',random.randint(10000,40000)))
        if filename == None:
            self.infile = sys.stdin
        else:
            self.infile = open(filename,"rb")

    # Waits until packet is received to return.
    def receive(self, timeout=None):
        self.sock.settimeout(timeout)
        try:
            return self.sock.recv(4096)
        except (socket.timeout, socket.error):
            return None

    # Sends a packet to the destination address.
    # Uses import.pickle to convert tuple packet
    # into a byte stream
    # It seemed the most efficient way to send
    # not only text files, but image files
    # All files are handled the same
    def send(self, message, address=None):
        if address is None:
            address = (self.dest,self.dport)
        pickledMsg = pickle.dumps(message)
        print(len(pickledMsg))
        self.sock.sendto(pickledMsg, address)

    def split_packet(self, message):
        body = message[0]
        msg_type, seqno = body[0:2]
        checksum = message[-1]
        return msg_type, seqno, checksum

    # Main sending loop.
    def start(self):
        raise NotImplementedError
