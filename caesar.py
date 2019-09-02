import random

class Caesar():
    def __init__(self, ran = random.randint(0, 9999)):
        self.key = ran % 95

    def encryption(self, plaintext):
        ciphertext = ''
        for letter in plaintext:
            pos = ord(letter) + self.key
            if pos > 126:
                pos = 32 + (pos - 126 - 1)
            ciphertext += chr(pos)
        return ciphertext, self.key

    def decryption(self, ciphertext, key):
        plaintext = ''
        for letter in ciphertext:
            pos = ord(letter) - key
            if pos < 32:
                pos = 126 - (32 - pos - 1)
            plaintext += chr(pos)
        return plaintext

if __name__ == '__main__':
    shift = random.randint(0,999)
    caesar = Caesar(shift)

    print("__Caesar Test Begin__")
    
    plaintext = "Hello Simon. Nice to meet you."
    print("Original Plaintext -> " + plaintext)
    
    ciphertext = caesar.encryption(plaintext)
    print("Ciphertext -> " + ciphertext)

    message = caesar.decryption(ciphertext)
    print("Received Message -> " + message)
    
    print("__Caesar Test End__")
