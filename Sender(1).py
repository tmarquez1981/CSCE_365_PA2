import sys
import getopt
import socket

import Checksum
import BasicSender
import Packet
import pickle

'''
This is a skeleton sender class. Create a fantastic transport protocol here.
'''
class Sender(BasicSender.BasicSender):
    
    
    # Main sending loop.
    def start(self):
        self.WINDOW_SIZE=4
        self.timeout=False
        self.current_state = 'start'
        self.errACKcount = 0
        self.iterCount = 0
        self.states={
            'start': self.fast_start,
            'erravd': self.error_avoid,
            'fast': self.fast_recovery
        }
        seqno=0
        while True:
            seqno = self.states.get(self.current_state)(seqno)
            if seqno == -1:
                break

    def fast_start(self, seqno):
        self.WINDOW_SIZE += 1
        eof, maxackno = self.send_window(seqno, self.WINDOW_SIZE)
        ackno = self.wait_window(seqno, maxackno)
        if self.errACKcount >= 2:
            self.reset_vars()
            self.current_state = 'fast'
        elif self.iterCount >= 2:
            self.reset_vars()
            self.current_state = 'erravd'
        if eof:
            return -1
        if ackno != -1:
            return ackno
        return seqno

    def error_avoid(self, seqno):
        eof, maxackno = self.send_window(seqno, self.WINDOW_SIZE)
        ackno = self.wait_window(seqno, maxackno)
        if self.errACKcount >= 2:
            self.reset_vars()
            self.current_state='fast'
        elif self.iterCount >= 2:
            self.reset_vars()
            self.current_state='start'
        if eof:
            return -1
        if ackno!=-1:
            return ackno
        return seqno

    def fast_recovery(self, seqno):
        if self.WINDOW_SIZE > 1:
            self.WINDOW_SIZE -= 1
        eof, maxackno = self.send_window(seqno, self.WINDOW_SIZE)
        ackno = self.wait_window(seqno, maxackno)
        if self.errACKcount >= 2:
            self.current_state = 'fast'
        else:
            self.current_state = 'erravd'
        self.reset_vars()
        if eof:
            return -1
        if ackno != -1:
            return ackno
        return seqno

    def reset_vars(self):
        self.errACKcount = 0
        self.iterCount = 0

   #sends MAX_WINDOW number of packets, returns eof=true/false and highest expected ackno
    def send_window(self, seqno, WINDOW_SIZE):
        maxseqno = seqno + self.WINDOW_SIZE
        self.iterCount += 1
        eof=False
        while seqno <= maxseqno and not eof:
            if seqno==0:
                eof = self.send_data('start',seqno)#special case of the first packet
            else:
                eof = self.send_data('data',seqno)
            seqno+=1
        if eof:
            seqno-=1
        return eof, seqno
            
    #read from file and send the data as a single packet
    def send_data(self,msgtype, seqno):
        self.infile.seek(seqno * 4000, 0)  # 4000B to account for bytes used by seqno, '|' chars, msgtype, and checksum; receiver takes 4096B
        data = self.infile.read(4000) # 4000B to account for bytes used by seqno, '|' chars, msgtype, and checksum; receiver takes 4096B
                                      # We chose 300 because picling the packets added some weight
        if not data:
            msgtype = 'end' # create end packet
            newPacket = Packet.Packet(msgtype, seqno, data)
            packet = newPacket.make_packet()
            self.send(packet)
            if self.debug:
                print('Sent # %d' % (seqno))
            return True
        else:
            newPacket = Packet.Packet(msgtype, seqno, data) # create a packet object to encapsulate the packet info
            packet = newPacket.make_packet()
            self.send(packet)
            if self.debug:
                print('Sent # %d' % (seqno))
        return False

    #gets acks from seqno -- seqnomax for ackno, returns highest seqno (to be used for next window)
    def wait_window(self, seqno, acknomax):
        ackno=0
        rcvdacknolist=[]
        acknolist=self.make_acknolist(seqno, acknomax)
        value = -1
        while not self.timeout:#no acks, re-transmit
            ackno = self.wait_ack()
            if self.debug:
                print('ack received for sequence number %d' % (ackno))
            if ackno == acknomax:#highest ack possible received
                del acknolist
                del rcvdacknolist
                return acknomax #this will be next seqno for send_window
            elif not ackno==-1:#if ack receive success
                index = self.get_index(acknolist,ackno)
                if index>=0:#if found in expected list
                    rcvdacknolist.append(ackno)#add to found list
                else:
                    self.errACKcount += 1
            else:
                self.errACKcount += 1
        if self.timeout:
            self.timeout=False
        value = self.get_largest(rcvdacknolist)
        del acknolist
        del rcvdacknolist
        return value
        
    #returns -1 if not found, or the index number
    def get_index(self, seqnolist, seqno):
        index=0
        while index<len(seqnolist):#
            if seqnolist[index] == seqno:
                return index
            index+=1
        return -1
    
    #returns a list of expected acknos
    def make_acknolist(self, start_seqno, acknomax):
        ackno=start_seqno+1#ackno is +1 from seqno
        acknolist=[]
        while ackno<=acknomax:
            acknolist.append(ackno)#not efficient but was quick to code, need to learn more python here
            ackno+=1
        return acknolist
        
    #returns highest number from list of ints
    def get_largest(self, integers):
        index=0
        value=-1
        index_max=len(integers)
        while index<index_max:
            if value<integers[index]:
                value=integers[index]
            index+=1
        return value        
                        
    #waits for a single ack, returning -1 if error or timeout, or ackno if success
    def wait_ack(self):
        if self.debug:
            print('waiting for ack')
        try:
            message = self.receive(0.5)
            message = pickle.loads(message)
            if message == None:
                return -1
            mtype, ackno, checksum = self.split_packet(message)
            if Checksum.validate_checksum(message):
                return int(ackno)
        except (socket.timeout, socket.error):
            self.timeout=True
        return -1

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
