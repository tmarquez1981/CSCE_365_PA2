import Checksum
import pickle

class Packet():
    def __init__(self, msg_type, seqno, data):
        self.msg_type = msg_type
        self.seqno = seqno
        self.data = data
        self.checksum = 0

    def make_packet(self):
        body = self.msg_type, self.seqno, self.data
        pickledBody = pickle.dumps(body)
        #body = "%s|%d|%s|" % (self.msg_type,self.seqno,self.data.decode())  # have to decode() to convert
        self.checksum = Checksum.generate_checksum(pickledBody)                    # byte file to string
        print("packet checksum = %s" % self.checksum)                       # prevents '\n' characters
        packet = body, self.checksum
        #packet = "%s%s" % (body, self.checksum)
        return packet
