#!/usr/bin/env python3
import base64
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.Hash import SHA256,MD5
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5


class RSACipher():
    """
    RSA Encryption, decryption, signature, signature verification tool class
    """
    def long_decrypt(self,private_key,msg):
        private_key =  ''.join([private_key[i:i+64]+'\n' for i in range(0, len(private_key), 64)])
        private_key = "-----BEGIN RSA PRIVATE KEY-----\n"+private_key+"-----END RSA PRIVATE KEY-----\n"
        msg = base64.b64decode(msg)
        length = len(msg)
        default_length = 128
        priobj = Cipher_pkcs1_v1_5.new(RSA.importKey(private_key))
        if length < default_length:
            return b''.join(priobj.decrypt(msg, b'xyz'))
        offset = 0
        res = []
        while length - offset > 0:
            if length - offset > default_length:
                res.append(priobj.decrypt(msg[offset:offset + default_length], b'xyz'))
            else:
                res.append(priobj.decrypt(msg[offset:], b'xyz'))
            offset += default_length
        print(b''.join(res).decode('utf8'))
        return b''.join(res).decode('utf8')


    def sign(self, private_key, text)->str:
        """
        Signature method
        :param key: private key
        :param text: Text requiring signature bytes
        :return: base64 Encoded signature information bytes
        """
        private_key =  ''.join([private_key[i:i+64]+'\n' for i in range(0, len(private_key), 64)])
        private_key = "-----BEGIN RSA PRIVATE KEY-----\n"+private_key+"-----END RSA PRIVATE KEY-----\n"
        
        private_key = RSA.importKey(private_key)
        hash_value = MD5.new(text.encode('utf-8'))
        signer = PKCS1_v1_5.new(private_key)
        signature = signer.sign(hash_value)
        return base64.b64encode(signature)