


# foundation.py 
# Foundation code for the stack. 
# This code is released to the public domain.  
# "Share and enjoy....."  :)



import socket
from protocol import parse_packet, packet_to_bytes

class Foundation:
    """
    A simple wrapper around a UDP socket for sending/receiving packets.
    This class just abstracts sending and receiving JSON packets.
    """

    def __init__(self, addr, is_server=False):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.addr = addr
        
        if is_server:
            self.sock.bind(addr)
            self.mode = "server"
        else:
            self.mode = "client"
        
        self.sock.settimeout(5.0)  # Set a timeout for simplicity

    def send_packet(self, packet: dict, dest_addr):
        data = packet_to_bytes(packet)
        self.sock.sendto(data, dest_addr)
    
    def receive_packet(self):
        data, addr = self.sock.recvfrom(65535)
        packet = parse_packet(data)
        return packet, addr



