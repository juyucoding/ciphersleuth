import math
import random
import os
import wsgiref.handlers
import json
import cryptomath
import sys

class AffineCipherTool:
	# Affine Cipher
	# http://inventwithpython.com/hacking (BSD Licensed)
	# made some modifications to source
	def __init__(self, mode, message,maxsize,lenofsym):
		self.mode = mode
		self.message = message
		self.name = 'affine'
		self.maxsize = maxsize
		self.SYMBOLS_str = """ !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\] ^_`abcdefghijklmnopqrstuvwxyz{|}~""" # note the space at the front
		self.SYMBOLS=len(self.SYMBOLS_str)
	key = 0
	def getRandomKey(self):
		while True:
			self.keyA = random.randint(2, self.SYMBOLS)
			self.keyB = random.randint(2, self.SYMBOLS)
			if cryptomath.gcd(self.keyA, self.SYMBOLS) == 1:
				self.key=self.keyA * self.SYMBOLS + self.keyB
				return self.keyA * self.SYMBOLS + self.keyB
	def storeKey(self,key):
		self.key = int(key)
		self.keyA, self.keyB = self.getKeyParts(self.key)
		self.badKey = self.checkKeys(self.keyA, self.keyB, 'encrypt')
		if self.okay == False:
			return False
		else:
			return True
	def getKey(self):
		while True:
			print('Would you like a randomly generated key?')
			ans = raw_input().lower()
			if ans[0] == 'y':
				self.key = self.getRandomKey()
				print(self.key)
			else:
				print('Enter the key number')
				key = int(raw_input())
				if (key >= 1 and key <= 65534):
					self.key = key
					self.keyA, self.keyB = self.getKeyParts(self.key)
					self.badKey = self.checkKeys(self.keyA, self.keyB, 'encrypt')
					if self.okay == True:
						return key
	def getKeyParts(self, key):
		self.keyA = key // self.SYMBOLS
		self.keyB = key % self.SYMBOLS
		return (self.keyA, self.keyB)
	def checkKeys(self, keyA, keyB, mode):
		self.okay = True
		if self.keyA == 1 and self.mode == 'e':
			self.okay = False
			return 'The affine cipher becomes incredibly weak when key A is set to 1. Choose a different key.'
		if self.keyB == 0 and self.mode == 'e':
			self.okay = False
			return 'The affine cipher becomes incredibly weak when key B is set to 0. Choose a different key.'
		if self.keyA < 0 or self.keyB < 0 or self.keyB > (self.SYMBOLS - 1):
			self.okay = False
			return 'Key A must be greater than 0 and Key B must be between 0 and %s.' % (self.SYMBOLS - 1)
		if cryptomath.gcd(self.keyA, self.SYMBOLS) != 1:
			self.okay = False
			return 'Key A (%s) and the symbol set size (%s) are not relatively prime. Choose a different key.' % (self.keyA, self.SYMBOLS)
	def getTranslatedMessage(self):
		if self.mode[0] == 'd':
			self.keyA, self.keyB = self.getKeyParts(self.key)
			self.checkKeys(self.keyA, self.keyB, 'decrypt')
			plaintext = ''
			modInverseOfKeyA = cryptomath.findModInverse(self.keyA, self.SYMBOLS)

			for symbol in self.message:
				if symbol in self.SYMBOLS_str:
				# decrypt this symbol
					symIndex = self.SYMBOLS_str.find(symbol)
					plaintext += self.SYMBOLS_str[(symIndex - self.keyB) * modInverseOfKeyA % self.SYMBOLS]
				else:
					plaintext += symbol # just append this symbol undecrypted
			return plaintext
		else:
			self.keyA, self.keyB = self.getKeyParts(self.key)
			self.checkKeys(self.keyA, self.keyB, 'encrypt')
			ciphertext = ''
			for symbol in self.message:
				if symbol in self.SYMBOLS_str:
				# encrypt this symbol
					symIndex = self.SYMBOLS_str.find(symbol)
					ciphertext += self.SYMBOLS_str[(symIndex * self.keyA + self.keyB) % self.SYMBOLS]
				else:
					ciphertext += symbol # just append this symbol unencrypted
			return ciphertext
#def main():
#	toolbox = CipherToolbox()
#	mod = toolbox.getMode()
#	print(mod)
#	mes = toolbox.getMessage()
#	print(mes)
#	aff = AffineCipherTool(mod,mes)
#	toolbox.tools.append(aff)
#	key = aff.getRandomKey()
#	print(key)
#	aff.getKey()
#	print(aff.key)
#	cipher = aff.getTranslatedMessage()
#	print(cipher)
	
#if __name__ == '__main__':
#  main()
