# Packet class
# This class handles all of the data packets
# sent to the Receiver
#

import Checksum
import pickle

class Packet():
    def __init__(self, msg_type, seqno, data):
        self.msg_type = msg_type
        self.seqno = seqno
        self.data = data
        self.checksum = 0

    # make_packet function takes the class information
    # i.e. [the msg_type, seqno, data, and checksum] = body,
    # encapsulates it into a pickle stream,
    # appends a checksum, and returns
    # a packet as a tuple as [body, checksum]
    def make_packet(self):
        body = self.msg_type, self.seqno, self.data
        pickledBody = pickle.dumps(body)
        self.checksum = Checksum.generate_checksum(pickledBody)
        print("packet checksum = %s" % self.checksum)
        packet = body, self.checksum
        return packet
