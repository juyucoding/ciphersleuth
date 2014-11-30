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
	def __init__(self, mode, message):
		self.mode = mode
		self.message = message
		self.name = 'affine'
		self.MAX_KEY_SIZE = len(self.message)
	SYMBOLS = """ !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\] ^_`abcdefghijklmnopqrstuvwxyz{|}~""" # note the space at the front
	key = 0
	def getRandomKey(self):
		while True:
			self.keyA = random.randint(2, len(self.SYMBOLS))
			self.keyB = random.randint(2, len(self.SYMBOLS))
			if cryptomath.gcd(self.keyA, len(self.SYMBOLS)) == 1:
				return self.keyA * len(self.SYMBOLS) + self.keyB
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
					self.checkKeys(self.keyA, self.keyB, 'encrypt')
					if self.okay == True:
						return key
	def getKeyParts(self, key):
		self.keyA = key // len(self.SYMBOLS)
		self.keyB = key % len(self.SYMBOLS)
		return (self.keyA, self.keyB)
	def checkKeys(self, keyA, keyB, mode):
		self.okay = True
		if self.keyA == 1 and self.mode == 'encrypt':
			self.okay = False
			print('The affine cipher becomes incredibly weak when key A is set to 1. Choose a different key.')
		if self.keyB == 0 and self.mode == 'encrypt':
			self.okay = False
			print('The affine cipher becomes incredibly weak when key B is set to 0. Choose a different key.')
		if self.keyA < 0 or self.keyB < 0 or self.keyB > len(self.SYMBOLS) - 1:
			self.okay = False
			print('Key A must be greater than 0 and Key B must be between 0 and %s.' % (len(self.SYMBOLS) - 1))
		if cryptomath.gcd(self.keyA, len(self.SYMBOLS)) != 1:
			self.okay = False
			print('Key A (%s) and the symbol set size (%s) are not relatively prime. Choose a different key.' % (self.keyA, len(self.SYMBOLS)))
	def getTranslatedMessage(self):
		if self.mode[0] == 'd':
			self.keyA, self.keyB = self.getKeyParts(self.key)
			self.checkKeys(self.keyA, self.keyB, 'decrypt')
			plaintext = ''
			modInverseOfKeyA = cryptomath.findModInverse(self.keyA, len(self.SYMBOLS))

			for symbol in self.message:
				if symbol in self.SYMBOLS:
				# decrypt this symbol
					symIndex = self.SYMBOLS.find(symbol)
					plaintext += self.SYMBOLS[(symIndex - self.keyB) * modInverseOfKeyA % len(self.SYMBOLS)]
				else:
					plaintext += symbol # just append this symbol undecrypted
			return plaintext
		else:
			self.keyA, self.keyB = self.getKeyParts(self.key)
			self.checkKeys(self.keyA, self.keyB, 'encrypt')
			ciphertext = ''
			for symbol in self.message:
				if symbol in self.SYMBOLS:
				# encrypt this symbol
					symIndex = self.SYMBOLS.find(symbol)
					ciphertext += self.SYMBOLS[(symIndex * self.keyA + self.keyB) % len(self.SYMBOLS)]
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