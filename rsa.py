#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random

# ask判断素数
def ifPrimeNum(n):
	flag = 0
	a = 2
	a1 = pow(a,n,n)
	a2 = pow(a,1,n)
	if a1 == a2:
		return 1
	else:
		return 0

# 取得一个随机素数
def getPrimeNum(size = 128):
	flag = 0
	while not flag:
		n = random.randrange(2**(size - 1), 2**size)
		# 剔除部分不可靠因子
		if (n%2 == 0 or n%3 == 0 or n%5 == 0 or n%7 == 0 or n%13 == 0):
			continue
		flag = ifPrimeNum(n)
	return n

#判断a\b是否互素
def ifRelativelyPrime(a,b):
	if a < b:
		a,b=b,a
	while b != 0:
		flag = a%b
		a = b
		b = flag
	if (a,b) == (1,0):
		return 1
	else:
		return 0

# 由欧拉n获得e
def getE(fy):
	flag = 1
	while flag:
		e = random.randrange(2**10,fy)
		if ifRelativelyPrime(e,fy) == 1:
			flag = 0
	return e

def getD(a,b):
	flag = b
	if (a < b):
		a,b = b,a
	x2 = 1;x1 = 0; y2 = 0; y1 = 1
	# 乘法逆元(获得乘法逆元的简单算法)
	while (b > 0):
		q = a//b
		r = a -q*b; x = x2 - q*x1; y = y2 - q*y1
		a = b; b = r; x2 = x1; x1 = x; y2 = y1; y1 = y
	if (y2 < 0):
		y2 = flag + y2
	return y2

class RSA():

	def __init__(self, ifInit = 1):
		if ifInit:
			p = getPrimeNum()
			q = getPrimeNum()
			# print('--- p = ',p); print('--- q = ',q)
			n = p * q
			# print('--- n = ',n)
			fy = (p - 1) * (q - 1)
			# print('--- fy = ',fy)
			e = getE(fy)
			d = getD(e, fy)
			self.pubKey = e, n
			self.priKey = d, n
		else:
			pass

	def encryption(self, plainText, pubKey):
	
		plainText = str(plainText)
		c = []

		for i in plainText:
			c.append ( pow(ord(i),pubKey[0],pubKey[1]))

		return c

	def decryption(self, cypherText,priKey):
		# cypherText = str(cypherText)
		m = []
		#h = []
		for i in cypherText:
			m.append(pow(i,priKey[0],priKey[1]))
			#h.append( int('pow(i,d,n)',16))
		a = ''
		for i in m:
			a = a + chr(i)
		return a


	# 签名
	def sign(self,encryptedMessage, priKey):
		# signature = pow(encryptedMessage,priKey[0],priKey[1])
		signature = self.encryption(encryptedMessage, priKey)
		return signature

	def verify(self,encryptedMessage,signature,pubKey):
		# if (encryptedMessage == pow(signature,pubKey[0], pubKey[1])):
		if (encryptedMessage == self.decryption(signature, pubKey)):
			return True
		else:
			return False

	# RSA整体
	def main(self):
		p = getPrimeNum()
		q = getPrimeNum()
		# print('--- p = ',p); print('--- q = ',q)
		n = p * q
		# print('--- n = ',n)
		fy = (p - 1) * (q - 1)
		# print('--- fy = ',fy)
		e = getE(fy)
		d = getD(e, fy)
		self.pubKey = e, n
		self.priKey = d, n
		# print("公钥： ",pubKey)
		# print("私钥： ",priKey)
		# k = []
		# k = input("请输入需要签名的信息：")
		# m = []
		# for i in k:
		# 	m.append(ord(i))
		# x = 0
		# for i in m:
		# 	x = x + i
		# y = sign(x,d,n)
		# verify(x,y,e,n)
		message = 'hello i am simon.how are you!!!@@@$$$###'
		# t = []
		t = self.encryption(message,self.pubKey)
		self.decryption(t,self.priKey)

if __name__ == "__main__":
	a = RSA()
	
# a.main()
