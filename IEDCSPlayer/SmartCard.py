from M2Crypto import X509
import PyKCS11


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
                    certs.append(certificate)
            return certs
        except Exception as e:
            print 'Error:', e
            return None

    def longToOct(self, data):
        # parse list of longs to octect string
        return ''.join(chr(s) for s in data)

    def veriStatus(self):

        veri = self.pkcs11.getSlotList()
        self.session = self.pkcs11.openSession(self.slots[0])
        print "ver", veri[0]
        if veri:
            return 0
        return 1

#CKR_TOKEN_NOT_PRESENT (0x000000E0)

#print "Found %d objects: %s" % (len(objects), [x.value() for x in objects])
# cenas = pteidGet(objects)
# print "User CC", cenas.getBI()
