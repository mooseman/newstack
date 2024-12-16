

# server.py 
# A toy proof-of-concept of a NUSP server.  
# This code is released to the public domain.  
# "Share and enjoy....."  :)  



import sys
from protocol import (
    VERSION, TYPE_HANDSHAKE_INIT, TYPE_HANDSHAKE_RESP, TYPE_HANDSHAKE_COMP, TYPE_DATA,
    create_handshake_resp_packet, create_data_packet
)
from foundation import Foundation
from crypto import generate_ephemeral_keys, derive_session_key, encrypt, decrypt

SERVER_SCID = "server123"
SERVER_ADDR = ("localhost", 55555)

class NUSPServer:
    def __init__(self, addr):
        self.foundation = Foundation(addr, is_server=True)
        self.server_private_key, self.server_public_key = generate_ephemeral_keys()
        
        self.session_key = None
        self.client_addr = None
        self.session_established = False

    def run(self):
        print(f"[Server] Listening on {self.foundation.addr}")
        while True:
            try:
                packet, addr = self.foundation.receive_packet()
            except:
                # Timeout or other error
                continue
            
            ptype = packet["type"]
            
            if ptype == TYPE_HANDSHAKE_INIT:
                self.handle_handshake_init(packet, addr)
            elif ptype == TYPE_HANDSHAKE_COMP:
                self.handle_handshake_complete(packet, addr)
            elif ptype == TYPE_DATA:
                self.handle_data(packet, addr)
    
    def handle_handshake_init(self, packet, addr):
        print(f"[Server] Received handshake init from {addr}")
        client_pub = packet["client_pub"].encode('latin1')
        
        self.session_key = derive_session_key(self.server_private_key, client_pub)
        self.client_addr = addr
        
        resp = create_handshake_resp_packet(self.server_public_key, SERVER_SCID)
        self.foundation.send_packet(resp, addr)
        print("[Server] Sent handshake response.")
    
    def handle_handshake_complete(self, packet, addr):
        if addr == self.client_addr and self.session_key is not None:
            print("[Server] Handshake completed, session established.")
            self.session_established = True
            
            # Send a welcome message as data
            plaintext = b"Hello from the server!"
            nonce, ciphertext = encrypt(self.session_key, plaintext)
            resp = create_data_packet(ciphertext, nonce)
            self.foundation.send_packet(resp, self.client_addr)
            print("[Server] Sent encrypted data.")
    
    def handle_data(self, packet, addr):
        if not self.session_established or addr != self.client_addr:
            print("[Server] Received data but session not established or wrong addr.")
            return
        
        ciphertext = packet["ciphertext"].encode('latin1')
        nonce = packet["nonce"].encode('latin1')
        
        try:
            plaintext = decrypt(self.session_key, nonce, ciphertext)
            print("[Server] Received message:", plaintext.decode('utf-8'))
            
            # Echo back a response
            response = b"Server echo: " + plaintext
            nonce, ciphertext = encrypt(self.session_key, response)
            resp = create_data_packet(ciphertext, nonce)
            self.foundation.send_packet(resp, self.client_addr)
            print("[Server] Sent encrypted data.")
        except:
            print("[Server] Decryption failed.")

if __name__ == "__main__":
    server = NUSPServer(SERVER_ADDR)
    server.run()



