import math
import random
import os
import wsgiref.handlers
import json
import sys


class SubstitutionCipherTool:
# Simple Substitution Cipher
# http://inventwithpython.com/hacking (BSD Licensed)
# made some modifications to source
	def __init__(self, mode, message):
		self.mode = mode
		self.message = message
		self.name = 'substitution'		
		self.LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
	def checkValidKey(self,key):
		keyList = list(key)
		lettersList = list(self.LETTERS)
		keyList.sort()
		lettersList.sort()
		result = False
		if keyList != lettersList:
			return result
		else:
			result = True
		return result
	def getKey(self):
		print('Input the 26-letter string of characters to use as a key:')
		self.key = raw_input()
		while self.checkValidKey(self.key) != True:
			print('That key is invalid. Please enter a new one:')
			self.key = raw_input()
		return self.key
	def storekey(self,keystr):
		self.key=keystr
	def getTranslatedMessage(self):
		translated = ''
		charsA = self.LETTERS
		charsB = self.key
		if self.mode[0] == 'd':
			charsA, charsB = charsB, charsA
		
		# loop through each symbol in the message
		for symbol in self.message:
			if symbol.upper() in charsA:
			# encrypt/decrypt the symbol
				symIndex = charsA.find(symbol.upper())
				if symbol.isupper():
					translated += charsB[symIndex].upper()
				else:
					translated += charsB[symIndex].lower()
			else:
				# symbol is not in LETTERS, just add it
				translated += symbol
		return translated
#def main():
#	toolbox = CipherToolbox()
#	mod = toolbox.getMode()
#	print(mod)
#	mes = toolbox.getMessage()
#	print(mes)
#	subs = SubstitutionCipherTool(mod,mes)
#	toolbox.tools.append(subs)
#	subs.getKey()
#	print(subs.key)
#	cipher = subs.getTranslatedMessage()
#	print(cipher)
	
#if __name__ == '__main__':
#  main()
