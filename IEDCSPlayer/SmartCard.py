# based on code from http://ludovicrousseau.blogspot.pt/

from M2Crypto import X509
# from M2Crypto import RSA, BIO
import PyKCS11
# from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA


class SmartCard(object):

    def __init__(self):

        self.pkcs11 = PyKCS11.PyKCS11Lib()
        self.pkcs11.load('/usr/local/lib/libpteidpkcs11.so')
        self.slots = None
        self.session = None
        self.objects = None

    # tries to open session with the smart card
    def startSession(self):
        self.slots = self.pkcs11.getSlotList()
        try:
            # slot 0:  where the info on the smartcard is
            self.session = self.pkcs11.openSession(self.slots[0])

            # loads the certificates and other data from smartcard
            self.objects = self.session.findObjects()
            return None
        except Exception as e:
            if "CKR_TOKEN_NOT_PRESENT" in str(e):
                return "Insert smart card on reader!\n"

            if ValueError:
                return "Connect the smart card reader!\n"

    def getCCNumber(self):
        certs = self.getUserCerts()
        if certs:
            for c in certs:
                # X509, as_text(): returns the name as a string.
                plain = str(c.as_text())
                begin = plain.find("serialNumber=BI")
                size = len("serialNumber=BI")
                # 8 = size of CC number
                return plain[begin + size:begin + size + 8]

    # Filter CA certificates
    def getUserCerts(self):
        # check_ca()-> Check if the certificate is a Certificate Authority (CA) certificate
        userCerts = [uc for uc in self.getAllCerts() if not uc.check_ca()]
        return userCerts

    def getAutenPubKey(self):

        user = self.getUserCerts()
        cert = user[0]
        pubkey = cert.get_pubkey()
        key = RSA.importKey(pubkey.as_der())
        # print key.publickey().exportKey() save to server
        return key


    # Get all certificates from pteid SmartCard
    def getAllCerts(self):
        try:
            certs = []
            for obj in self.objects:
                data = obj.to_dict()
                # CKO_CERTIFICATE: hold public-key or attribute certificates
                if data['CKA_CLASS'] == 'CKO_CERTIFICATE':
                    raw = self.longToOct(data['CKA_VALUE'])
                    certificate = X509.load_cert_string(raw, X509.FORMAT_DER)
                    certificate.verify()
                    certs.append(certificate)
            return certs
        except Exception as e:
            print 'Error:', e
            return None

    def longToOct(self, data):
        # parse list of longs to octect string
        return ''.join(chr(s) for s in data)

    def signData(self, data=None):

        if self.session is not None:

            try:
                print "Login Pteid..."
                self.session.login('')
            except Exception as e:
                print "Login failed", e

            self.objects = self.session.findObjects()
            all_attributes = PyKCS11.CKA.keys()

            # remove the CKR_ATTRIBUTE_SENSITIVE attributes since we can't get
            # their values and will get an exception instead
            all_attributes.remove(PyKCS11.CKA_PRIVATE_EXPONENT)
            all_attributes.remove(PyKCS11.CKA_PRIME_1)
            all_attributes.remove(PyKCS11.CKA_PRIME_2)
            all_attributes.remove(PyKCS11.CKA_EXPONENT_1)
            all_attributes.remove(PyKCS11.CKA_EXPONENT_2)
            all_attributes.remove(PyKCS11.CKA_COEFFICIENT)
            # only use the integer values and not the strings like 'CKM_RSA_PKCS'
            all_attributes = [e for e in all_attributes if isinstance(e, int)]

            for o in self.objects:
                attributes = self.session.getAttributeValue(o, all_attributes)
                attrDict = dict(zip(all_attributes, attributes))
                if attrDict[PyKCS11.CKA_CLASS] == PyKCS11.CKO_PRIVATE_KEY \
                   and attrDict[PyKCS11.CKA_KEY_TYPE] == PyKCS11.CKK_RSA and attrDict[PyKCS11.CKA_LABEL] == 'CITIZEN AUTHENTICATION KEY':

                    try:
                        toSign = "12345678901234567890"  # 20 bytes, SHA1 digest
                        signature = self.session.sign(o, toSign)
                        self.veriSign(signature, toSign)

                    except Exception as e:
                        print "Sign failed, exception: ", e

    def veriSign(self, signature, data):
        key = self.getAutenPubKey()
        modulus = key.n
        exponent = key.e

        if modulus and exponent:
            s = ''.join(chr(c) for c in signature).encode('hex')
            sx = eval('0x%s' % s)

            decrypted = pow(sx, exponent, modulus)  # RSA
            # print "Decrypted:"
            d = self.hexx(decrypted).decode('hex')
            # print self.dump(d, 16)
            if data == d[-20:]:
                print "Signature VERIFIED!\n"
            else:
                print "Signature NOT VERIFIED!"
        else:
            print "Unable to verify signature: MODULUS/PUBLIC_EXP not found"

    def hexx(self, intval):
        x = hex(intval)[2:]
        if x[-1:].upper() == 'L':
            x = x[:-1]
        if len(x) % 2 != 0:
            return "0%s" % x
        return x

    def dump(self, src, length=8):
        FILTER = ''.join([(len(repr(chr(x))) == 3) and chr(x) or '.' for x in range(256)])
        N = 0
        result = ''
        while src:
            s, src = src[:length], src[length:]
            hexa = ' '.join(["%02X" % ord(x) for x in s])
            s = s.translate(FILTER)
            result += "%04X   %-*s   %s\n" % (N, length * 3, hexa, s)
            N += length
        return result






#CKR_TOKEN_NOT_PRESENT (0x000000E0)

#print "Found %d objects: %s" % (len(objects), [x.value() for x in objects])
# cenas = pteidGet(objects)
# print "User CC", cenas.getBI()
