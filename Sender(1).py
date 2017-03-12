import sys
import getopt

import Checksum
import BasicSender

'''
This is a skeleton sender class. Create a fantastic transport protocol here.
'''
class Sender(BasicSender.BasicSender):
    # Main sending loop.
    def start(self):
        self.seqno=0
        success = self.send_data('start', self.seqno)#needs a start packet first
        while success:
            success = self.send_data('data', self.seqno)#breaks when eof; 'end' packet not yet implemented
            if success and self.debug:
                print 'success: sent sequence number %d' % (self.seqno)
        

    def send_data(self,msgtype, seqno):
        data = self.infile.read(4076)#header varies from 18-20B; packet size total = 4096
        if data == '':              #also need to make sure when packets are resent we seek
            return False            # to correct position
        else:
            packet = self.make_packet(msgtype,seqno,data)
            self.send(packet)
            self.seqno=seqno+1
            while not self.wait_ack(self.seqno): #remove when sliding window implemented, we'll have to do ack differtently
                self.send(packet)
        return True


    def wait_ack(self, expseqno):
        if self.debug:
            print 'waiting for ack %d' % (expseqno)
        message = self.receive()
        mtype, seqno, checksum, extra = self.split_packet(message)
        if self.debug:
            print 'ack received for sequence number ' + seqno
        if Checksum.validate_checksum(message) and expseqno==int(seqno):
            return True
        return False

'''
This will be run if you run this script from the command line. You should not
change any of this; the grader may rely on the behavior here to test your
submission.
'''
if __name__ == "__main__":
    def usage():
        print ("Sender")
        print ("-f FILE | --file=FILE The file to transfer; if empty reads from STDIN")
        print ("-p PORT | --port=PORT The destination port, defaults to 33122")
        print ("-a ADDRESS | --address=ADDRESS The receiver address or hostname, defaults to localhost")
        print ("-d | --debug Print debug messages")
        print ("-h | --help Print this usage message")

    try:
        opts, args = getopt.getopt(sys.argv[1:],
                               "f:p:a:d", ["file=", "port=", "address=", "debug="])
    except:
        usage()
        exit()

    port = 33122
    dest = "localhost"
    filename = None
    debug = False

    for o,a in opts:
        if o in ("-f", "--file="):
            filename = a
        elif o in ("-p", "--port="):
            port = int(a)
        elif o in ("-a", "--address="):
            dest = a
        elif o in ("-d", "--debug="):
            debug = True

    s = Sender(dest,port,filename,debug)
    try:
        s.start()
    except (KeyboardInterrupt, SystemExit):
        exit()
