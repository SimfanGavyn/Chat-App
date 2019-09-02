# origin = [
#     'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',
#     'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
#     'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a',  
#     'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 
#     'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 
#     't', 'u', 'v', 'w', 'x', 'y', 'z', '{', ':', 
#     '}', '~', '!', '\"', '#', '$', '%', '&', '\'', 
#     '<', '>', '*', '+', ',', '-', '.', '/', '0', 
#     '1', '2', '3', '4', '5', '6', '7', '8', '9' 
# ]

# matrix = []

import random

# def generateKey(origin):
#     k = ''
#     round = random.randint(0, 40)
#     for i in range(round):
#         c = origin[random.randint(0, 80)]
#         if k.count(c) == 0:
#             k += c
#     return k

class Playfair():
    # origin = [
    #     'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',
    #     'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
    #     'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a',  
    #     'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 
    #     'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 
    #     't', 'u', 'v', 'w', 'x', 'y', 'z', '{', ':', 
    #     '}', '~', '!', '\"', '#', '$', '%', '&', '\'', 
    #     '<', '>', '*', '+', ',', '-', '.', '/', '0', 
    #     '1', '2', '3', '4', '5', '6', '7', '8', '9' 
    # ]

    # matrix = []

    def __init__(self, ifInit = 1):
        # self.__main__()
        self.origin = [
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',
            'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
            'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a',  
            'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 
            'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 
            't', 'u', 'v', 'w', 'x', 'y', 'z', '{', ':', 
            '}', '~', '!', '\"', '#', '$', '%', '&', '\'', 
            '<', '>', '*', '+', ',', '-', '.', '/', '0', 
            '1', '2', '3', '4', '5', '6', '7', '8', '9' 
        ]
        self.matrix = []
        if ifInit:
            self.key = self.generateKey()
            self.generateMatrix(self.key)
        else:
            pass
    
    # def __main__(self):
    #     # key = ''
    #     # self.origin = [
    #     #     'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',
    #     #     'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
    #     #     'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a',  
    #     #     'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 
    #     #     'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 
    #     #     't', 'u', 'v', 'w', 'x', 'y', 'z', '{', ':', 
    #     #     '}', '~', '!', '\"', '#', '$', '%', '&', '\'', 
    #     #     '<', '>', '*', '+', ',', '-', '.', '/', '0', 
    #     #     '1', '2', '3', '4', '5', '6', '7', '8', '9' 
    #     # ]
    #     # self.matrix = []

    #     self.key = self.generateKey()
    #     self.generateMatrix(self.key)

    def generateKey(self):
        k = ''
        round = random.randint(0, 20)
        for i in range(round):
            r = random.randint(0, 80)
            # print("r: " + str(r), len(self.origin), round)
            
            c = self.origin[r]
            if k.count(c) == 0:
                k += c
        return k

    def generateMatrix(self, key):
        # global matrix
        k = str(key)
        for i in key:
            self.origin.remove(i)
        for i in self.origin:
            k += i
        self.matrix = list(k)
        # print(matrix, len(matrix))

    def encryption(self, plaintext):
        matrix = self.matrix
        temp = ''
        for i in range(len(plaintext)):
            letter = plaintext[i]
            if plaintext[i] == ' ':
                letter = 'BMW'
            elif i + 1 < len(plaintext) and plaintext[i] == plaintext[i + 1]:
                letter = 'AOX'
            temp += letter
        if len(plaintext) % 2 == 1:
            temp += 'AOX'
        ciphertext = ''
        for i in range(0, len(temp), 2):
            pos_1 = matrix.index(temp[i])
            pos_2 = matrix.index(temp[i + 1])
            if pos_1 % 9 == pos_2 % 9:  #同一列 未处理 AAOX
                pos_1 += 9
                if pos_1 > 80:
                    pos_1 -= 81
                pos_2 += 9
                if pos_2 > 80:
                    pos_2 -= 81
                ciphertext += matrix[pos_1]
                ciphertext += matrix[pos_2]
            elif pos_1 / 9 == pos_2 / 9:
                round = pos_1 / 9
                pos_1 += 1
                if pos_1 / 9 != round:
                    pos_1 -= 9
                pos_2 += 1
                if pos_2 / 9 != round:
                    pos_2 -= 9
                ciphertext += matrix[pos_1]
                ciphertext += matrix[pos_2]
            else:
                row_1 = int(pos_1 / 9)
                col_1 = pos_1 - int(pos_1 / 9) * 9
                row_2 = int(pos_2 / 9)
                col_2 = pos_2 - int(pos_2 / 9) * 9
                pos_1 = int(row_1 * 9 + col_2)
                pos_2 = int(row_2 * 9 + col_1)
                ciphertext += matrix[pos_1]
                ciphertext += matrix[pos_2]
        return ciphertext, self.key

    def decryption(self, ciphertext):
        matrix = self.matrix
        temp = ''
        for i in range(0, len(ciphertext), 2):
            pos_1 = matrix.index(ciphertext[i])
            pos_2 = matrix.index(ciphertext[i + 1])
            if pos_1 % 9 == pos_2 % 9:  #同一列 未处理 AAOX
                pos_1 -= 9
                if pos_1 < 0:
                    pos_1 += 81
                pos_2 -= 9
                if pos_2 < 0:
                    pos_2 += 81
                temp += matrix[pos_1]
                temp += matrix[pos_2]
            elif pos_1 / 9 == pos_2 / 9:
                round = pos_1 / 9 #同一行
                pos_1 -= 1
                if pos_1 / 9 != round:
                    pos_1 += 9
                pos_2 -= 1
                if pos_2 / 9 != round:
                    pos_2 += 9
                temp += matrix[pos_1]
                temp += matrix[pos_2]
            else:
                row_1 = int(pos_1 / 9)
                col_1 = pos_1 - int(pos_1 / 9) * 9
                row_2 = int(pos_2 / 9)
                col_2 = pos_2 - int(pos_2 / 9) * 9
                pos_1 = int(row_1 * 9 + col_2)
                pos_2 = int(row_2 * 9 + col_1)
                temp += matrix[pos_1]
                temp += matrix[pos_2]
        i = 0
        plaintext = ''
        while(i < len(temp)):
            letter = temp[i]
            if temp[i] == 'B' and i + 2 < len(temp) and temp[i + 1] == 'M' and temp [i + 2] == 'W':
                letter = ' '
                i += 3
            elif temp[i] == 'A' and i + 2 == len(temp) - 1 and temp[i + 1] == 'O' and temp [i + 2] == 'X':
                letter = ''
                break
            elif temp[i] == 'A' and i + 2 < len(temp) and temp[i + 1] == 'O' and temp [i + 2] == 'X':
                round = True
                times = 0
                while round:
                    if temp[i] == 'A' and i + 2 < len(temp) and temp[i + 1] == 'O' and temp [i + 2] == 'X':
                        i += 3
                        times += 1
                    else:
                        round = False
                        letter = ''
                        for j in range(times + 1):
                            letter += temp[i]
                        i += 1
            else:
                i += 1
            plaintext += letter
        return plaintext

if __name__ == "__main__":
    p = Playfair()
    pt = 'hello i am simon how are you'
    ct, key = p.encryption(pt)
    print("ct: " + ct)
    print("Matrix: " + str(p.matrix))
    print("key: " + key)
    pp = Playfair(0)
    print("Origin: " + str(pp.origin))
    pp.generateMatrix(key)
    mes = pp.decryption(ct)
    print("mes" + mes)
    
