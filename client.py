

# client.py 
# A toy proof-of-concept of a NUSP client.  
# This code is released to the public domain.  
# "Share and enjoy....."  :)  



import time
from protocol import (
    VERSION, TYPE_HANDSHAKE_INIT, TYPE_HANDSHAKE_RESP, TYPE_HANDSHAKE_COMP, TYPE_DATA,
    create_handshake_init_packet, create_handshake_comp_packet, create_data_packet
)
from foundation import Foundation
from crypto import generate_ephemeral_keys, derive_session_key, encrypt, decrypt

CLIENT_SCID = "clientABC"
SERVER_ADDR = ("localhost", 55555)

class NUSPClient:
    def __init__(self, server_addr):
        self.server_addr = server_addr
        self.foundation = Foundation(("localhost", 0), is_server=False)  # ephemeral client port
        
        self.client_private_key, self.client_public_key = generate_ephemeral_keys()
        self.session_key = None
        self.session_established = False
    
    def run(self):
        print("[Client] Starting handshake...")
        self.send_handshake_init()
        
        try:
            packet, addr = self.foundation.receive_packet()
            if packet["type"] == TYPE_HANDSHAKE_RESP:
                self.handle_handshake_resp(packet, addr)
            
            self.send_handshake_complete()
            
            # Now session is established, send a test message
            time.sleep(0.5)
            self.send_data(b"Hello Secure World!")
            
            packet, addr = self.foundation.receive_packet()
            self.handle_data(packet, addr)
        except:
            print("[Client] Handshake or response timed out.")
    
    def send_handshake_init(self):
        init_packet = create_handshake_init_packet(self.client_public_key)
        self.foundation.send_packet(init_packet, self.server_addr)
        print("[Client] Sent handshake init.")
    
    def handle_handshake_resp(self, packet, addr):
        print("[Client] Received handshake response.")
        server_pub = packet["server_pub"].encode('latin1')
        self.session_key = derive_session_key(self.client_private_key, server_pub)
    
    def send_handshake_complete(self):
        comp_packet = create_handshake_comp_packet()
        self.foundation.send_packet(comp_packet, self.server_addr)
        print("[Client] Sent handshake complete.")
        self.session_established = True
    
    def send_data(self, plaintext):
        if not self.session_established or self.session_key is None:
            print("[Client] Session not established, cannot send data.")
            return
        nonce, ciphertext = encrypt(self.session_key, plaintext)
        data_packet = create_data_packet(ciphertext, nonce)
        self.foundation.send_packet(data_packet, self.server_addr)
        print("[Client] Sent encrypted data.")
    
    def handle_data(self, packet, addr):
        if not self.session_established:
            print("[Client] Received data but session not established.")
            return
        nonce = packet["nonce"].encode('latin1')
        ciphertext = packet["ciphertext"].encode('latin1')
        
        try:
            plaintext = decrypt(self.session_key, nonce, ciphertext)
            print("[Client] Received from server:", plaintext.decode('utf-8'))
        except:
            print("[Client] Decryption failed.")

if __name__ == "__main__":
    client = NUSPClient(SERVER_ADDR)
    client.run()




