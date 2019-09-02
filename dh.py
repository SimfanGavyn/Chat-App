from rsa import getPrimeNum

class DH():
    
    def getPAndG(self):
        p = getPrimeNum()
        for i in range(2, 20):
            if pow(i, p - 1, p) == 1:
                g = i
                break
        return p, g
    


