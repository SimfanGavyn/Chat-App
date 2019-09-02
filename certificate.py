import random

class Certificate():
    
    eType = {
        '1': 'caesar',
        '2': 'playfair',
        '3': 'des',
        '4': '3des'
    }

    cType = {
        '1': 'rsa',
        '2': 'dh'
    }

    def __init__(self, pubKey):
        self.certificateInfo = {
            # 'username': userName,
            'type': 'certificate',
            # 'encryptionType': 'playfair',
            'encryptionType': self.__randomEncryptionType(),
            'publicKey': pubKey,
            # 'communicationType': 'rsa'
            'communicationType': self.__randomCommunicationType()
        }

    def __randomEncryptionType(self):
        return self.eType[str(random.randint(1, 4))]

    def __randomCommunicationType(self):
        return self.cType[str(random.randint(1, 2))]

if __name__ == "__main__":
    random.randint(1, 4)
    c = Certificate('simon', 123456)
    print(c.certificateInfo)
