from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
import Crypto.Random as Random



class CryptoModule(object):
    # cypher_text = ""
    # plain_text = ""
    rsaKeyPub = ""
    rsaKeyPriv = ""


    """
        RSA encrypt
    """
    def rsaEncrypt(self, data):
        rsaKey = RSA.generate(2048, Random.new().read)
        self.rsaKeyPriv = rsaKey.has_private()
        # rsaKeyPub = rsaKey.publickey()
        encrypted = rsaKey.encrypt(data, 32)
        return encrypted


    """
        cypherAES method
    """
    def cipherAES(self, key, data):
        # Encryption mode
        encryption_suite = AES.new(key, AES.MODE_CFB, 'This is an IV456')
        # data = "A really secret message. Not for prying eyes."
        # encrypt
        cipher_text = encryption_suite.encrypt(data)
        return cipher_text


    """
        decypherAES method
    """
    def decipherAES(self, key, data):
        # Decryption
        decryption_suite = AES.new(key, AES.MODE_CFB, 'This is an IV456')
        plain_text = decryption_suite.decrypt(data)
        return plain_text


    """
        hashing method
    """
    def hashingSHA256(self, data):
        h = SHA256.new()
        h.update(data)
        return h.digest()



c = CryptoModule()

# print c.rsaKeyPub
# print c.rsaKeyPriv

print c.rsaEncrypt("ola")
