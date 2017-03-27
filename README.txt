Computer Networks A365 Assignment 2
UDP FTP with TCP Reliability
by Benjamin Gurganious and Thomas Marquez
Github Project URL: https://github.com/tmarquez1981/CSCE_365_PA2

Purpose:
The purpose of this assignment was to make a simple UDP file-transfer program with TCP reliability implementation. The application must account for packet loss, delay, corruption, duplication, and reordering. 

Implementation:
We built on the files provided by Dr. Butler. The provided classes provided were the Receiver, BasicSender, Sender, and Checksum. The majority of our work was done to the Sender class, with some minor modifications to the Receiver, BasicSender, and the Checksum class. We also added a Packet class which handles the data packets sent from the Sender. 

Our implementation of the assignment closely follows the TCP state machine from the textbook  Computer Networking, A Top-Down Approach by James Kurose and Keith Ross. The state machine diagram can be found on page 274. 

In the Sender class, we implemented a TCP congestion control state machine with three states, a fast-start state, an error-avoid state, and a fast-recovery state. 

We used import.pickle to convert the packets into a byte stream. 

Running the Program:
Running of the program follows the specified guidelines. All input is done from the command line. The Receiver will print the packet received including the data ,which could be a lot of information depending on the size of the file. The Sender will display the sequence number sent including the size of the packet sent, and also the received ACK from the Receiver. 

Diversion From Assignment Requirements:
The assignment requirements state that the format of the sent data from the Sender should be in the following format: msg_type|<seqno>|<data>|<checksum>. Although our packets do follow the general format, we omitted the ‘|’ separating the messages to allow for packets to be sent as a tuple instead of a string. This allowed us to easily handle various file types, such as text and images files, with ease. 

With our packets in a tuple, we pickled the packets after creation and sent it over the network. 

With this change, however, we had to make a few changes to the Receiver, the BasicSender, and the Checksum to allow for packets to be received as tuples as oppose to a string with ‘|’ delimiters. But since the messages were sent in the same order, the conversion was pretty straight forward. 

More information can be found on the Github repository, including branches where we did most of our changes, as well as some UML designs we made earlier on in the project. 

