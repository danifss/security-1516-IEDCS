# -*- coding: utf-8 -*-
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
import Crypto.Random as Random
import hashlib



class CryptoModule(object):
    # cypher_text = ""
    # plain_text = ""
    rsaKeyPub = ""
    rsaKeyPriv = ""


    """
        RSA encrypt
    """
    def rsaKeys(self, data):
        rsaKey = RSA.generate(2048)

        # self.rsaKeyPriv = rsaKey.has_private()
        # rsaKeyPub = rsaKey.publickey()
        # encrypted = rsaKey.encrypt(data, 32)
        #return rsaKey


    """
        cypherAES method
    """
    def cipherAES(self, key, vi, data):
        # Encryption mode
        encryption_suite = AES.new(key, AES.MODE_CFB, vi)
        # encrypt
        cipher_text = encryption_suite.encrypt(data)
        return cipher_text


    """
        decypherAES method
    """
    def decipherAES(self, key, vi, data):
        # Decryption mode
        decryption_suite = AES.new(key, AES.MODE_CFB, vi)
        # decrypt
        plain_text = decryption_suite.decrypt(data)
        return plain_text


    """
        hashing method
    """
    def hashingSHA256(self, data):
        d = str.encode(data)
        type(d) # insures its bytes
        # apply sintese
        hash_object = hashlib.sha256(d)
        hex_dig = hash_object.hexdigest()

        return hex_dig




# f = CryptoModule()

### Testing RSA
# f.rsaKeys("a")


### Testing SHA256
# print f.hashingSHA256("ola mundo")

### Testing AES
vi = "jugujugleswagger"
#    cipherAES(key, vi, data)
c = f.cipherAES("_swaggerswagger_", vi, "isto e um espetaculo")
print "Cifra: " + c
p = f.decipherAES("_swaggerswagger_", vi, c)
print "Plain text: " + p
