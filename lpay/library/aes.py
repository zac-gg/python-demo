#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
python3 - AES SHA1PRNG
Note that the following dependent libraries need to be installed：
pip3 install pycryptodome
pip3 install Crypto
'''

from Crypto.Cipher import AES
import hashlib 
import base64 


BS = AES.block_size

def padding_pkcs5(value):
    return str.encode(value + (BS - len(value) % BS) * chr(BS - len(value) % BS))

# Convert decimal to hexadecimal
def get_sha1prng_key(key):
    signature = hashlib.sha1(key.encode()).digest()
    signature = hashlib.sha1(signature).digest()
    return ''.join(['%02x' % i for i in signature]).upper()[:32]

# encryption
def encrypt(key:str,value:str) -> str:
    cryptor = AES.new(bytes.fromhex(key), AES.MODE_ECB)
    padding_value = padding_pkcs5(value)  # padding content with pkcs5
    ciphertext = cryptor.encrypt(padding_value)
    ciphertext = base64.b64encode(ciphertext)
    return ciphertext
    #return ''.join(['%02x' % i for i in ciphertext]).upper()

# decrypt
def decrypt(key:str, value:str) -> str:
    ''' AES/ECB/NoPadding decrypt '''
    value = base64.b64decode(value)
    key = bytes.fromhex(key)
    cryptor = AES.new(key, AES.MODE_ECB)
    #ciphertext = cryptor.decrypt(bytes.fromhex(value))
    ciphertext = cryptor.decrypt(value)
    return padding_zero(str(ciphertext, "utf-8"))

# String processing, filtering special characters
def padding_zero(value):
    list = []
    for c in value:
        # Acquisition of ASCII code range
        if ord(c) > 31 & ord(c) < 127:
            list.append(c)
    return ''.join(list)