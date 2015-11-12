# -*- coding: utf-8 -*-
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
import Crypto.Random as Random
import hashlib
from base64 import b64decode



class CryptoModule(object):

    def __init__(self):
        self.rsaKeyPriv = ""
        self.rsaKeyPub = ""
        # cypher_text = ""
        # plain_text = ""


    """
        RSA generate
    """
    # returns rsa key object
    def generateRsa(self):

        pairKey = RSA.generate(2048)

        return pairKey

    """
        RSA public key
    """
    # returns public key object
    def publicRsa(self, pairKey):

        try:
            pairKey.can_encrypt()
        except Exception:
            print "Key not valid"

        return pairKey.publickey()

    """
        RSA public and private
    """
    #
    def pairRsa(self, pairKey):

        try:
            pairKey.can_encrypt()
            # check if is pair and not only public key
            pairKey.has_private()
        except Exception:
            print "Key not valid"
            return 1

        # Construct a new key carrying only the public information.
        # public = rsaKey.publickey()
        # Retrives data of the public key, format PEM
        # pub = public.exportKey()

        # Retrives data of the public key, format PEM
        pub = pairKey.publickey().exportKey('PEM')
        # Retrives data of the private key, format PEM
        priv = pairKey.exportKey('PEM')

        # # cifrar directamente com a chave publica, e decifrar com a chave rsa
        # x = pairKey.publickey()
        # encry = x.encrypt('encripta tudo',32)
        # dec = pairKey.decrypt(encry)
        # print encry
        # print dec

        return pub, priv

    """
        RSA ciphering
    """
    # receives rsa key, returns ciphered text
    def rsaCipher(self, pairKey, data):

        # import from file
        # pairKey = RSA.importKey(key)
        cipher = PKCS1_OAEP.new(pairKey)
        ciphertext = cipher.encrypt(data)

        # base64 turns the symbols of the ciphered text to "readable letters"
        return ciphertext.encode('base64')

    """
        RSA DEciphering
    """
    def rsaDecipher(self, pairKey, data):

        try:
            pairKey.can_encrypt()
            # check if is pair and not only public key
            pairKey.has_private()
        except Exception:
            print "Key not valid"
            return 1

        cipher = PKCS1_OAEP.new(pairKey)
        # if ciphertext was produced with base64, reverve using b64decode
        return cipher.decrypt(b64decode(data))


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


f = CryptoModule()


### Testing RSA
key = f.generateRsa()


data = 'bamos a esto'
cifrado = f.rsaCipher(key,data)
print cifrado

key2 = f.generateRsa()

wrongkey='dsad'
clear = f.rsaDecipher(wrongkey, cifrado)
print clear

### Testing SHA256
# print f.hashingSHA256("ola mundo")

# ### Testing AES
# vi = "jugujugleswagger"
# # random vi
# # vi = Random.new().read(AES.block_size)
# #    cipherAES(key, vi, data)
# c = f.cipherAES("_swaggerswagger_", vi, "isto e um espetaculo")
# print "Cifra: " + c
# p = f.decipherAES("_swaggerswagger_", vi, c)
# print "Plain text: " + p
