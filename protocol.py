


# protocol.py 
# Code for the NUSP protocol 
# This code is released to the public domain.  
# "Share and enjoy....."  :)



import json

# Protocol version and packet types
VERSION = 1
TYPE_HANDSHAKE_INIT = 0x01
TYPE_HANDSHAKE_RESP = 0x02
TYPE_HANDSHAKE_COMP = 0x03
TYPE_DATA = 0x10

def create_handshake_init_packet(client_public_key: bytes):
    return {
        "version": VERSION,
        "type": TYPE_HANDSHAKE_INIT,
        "client_pub": client_public_key.decode('latin1')
    }

def create_handshake_resp_packet(server_public_key: bytes, server_scid: str):
    return {
        "version": VERSION,
        "type": TYPE_HANDSHAKE_RESP,
        "server_pub": server_public_key.decode('latin1'),
        "server_scid": server_scid
    }

def create_handshake_comp_packet():
    return {
        "version": VERSION,
        "type": TYPE_HANDSHAKE_COMP
    }

def create_data_packet(ciphertext: bytes, nonce: bytes):
    return {
        "version": VERSION,
        "type": TYPE_DATA,
        "nonce": nonce.decode('latin1'),
        "ciphertext": ciphertext.decode('latin1')
    }

def parse_packet(data: bytes):
    # Expects a JSON-encoded packet
    packet = json.loads(data.decode('utf-8'))
    return packet

def packet_to_bytes(packet: dict):
    return json.dumps(packet).encode('utf-8')




