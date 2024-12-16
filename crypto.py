

# crypto.py 
# Encrytion and decryption for the stack. 
# This code is released to the public domain.  
# "Share and enjoy....."  :)


import os
from cryptography.hazmat.primitives.asymmetric import x25519
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

def generate_ephemeral_keys():
    private_key = x25519.X25519PrivateKey.generate()
    public_key = private_key.public_key().public_bytes()
    return private_key, public_key

def derive_session_key(private_key: x25519.X25519PrivateKey, peer_public_key: bytes):
    peer_pub = x25519.X25519PublicKey.from_public_bytes(peer_public_key)
    shared_secret = private_key.exchange(peer_pub)
    # In real code, use a KDF here.
    return shared_secret[:32]

def encrypt(session_key: bytes, plaintext: bytes):
    aesgcm = AESGCM(session_key)
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, plaintext, None)
    return nonce, ciphertext

def decrypt(session_key: bytes, nonce: bytes, ciphertext: bytes):
    aesgcm = AESGCM(session_key)
    return aesgcm.decrypt(nonce, ciphertext, None)


