import math
import random
import os
import wsgiref.handlers
import json
import sys

class VigenereCipherTool:
	# Vigenere Cipher (Polyalphabetic Substitution Cipher)
	# http://inventwithpython.com/hacking (BSD Licensed)
	# made some modifications to source
	def __init__(self, mode, message):
		self.mode = mode
		self.message = message
		self.name = 'vigenere'
	LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
	def storekey(self,key):
		self.key=key
	def getKey(self):
		print('Input a string of letters to use as a key:')
		self.key = raw_input()
		return self.key	
	def getTranslatedMessage(self):
		translated = [] # stores the encrypted/decrypted message string
		keyIndex = 0
		self.key = self.key.upper()

		for symbol in self.message: # loop through each character in message
			num = self.LETTERS.find(symbol.upper())
			if num != -1: # -1 means symbol.upper() was not found in LETTERS
				if self.mode[0] == 'e':
					num += self.LETTERS.find(self.key[keyIndex]) # add if encrypting
				elif self.mode[0] == 'd':
					num -= self.LETTERS.find(self.key[keyIndex]) # subtract if decrypting
	
				num %= len(self.LETTERS) # handle the potential wrap-around
	
				# add the encrypted/decrypted symbol to the end of translated.
				if symbol.isupper():
					translated.append(self.LETTERS[num])
				elif symbol.islower():
					translated.append(self.LETTERS[num].lower())

				keyIndex += 1 # move to the next letter in the key
				if keyIndex == len(self.key):
					keyIndex = 0
			else:
				# The symbol was not in LETTERS, so add it to translated as is.
				translated.append(symbol)
		return ''.join(translated)
#def main():
#	toolbox = CipherToolbox()
#	mod = toolbox.getMode()
#	print(mod)
#	mes = toolbox.getMessage()
#	print(mes)
#	vig = VigenereCipherTool(mod,mes)
#	toolbox.tools.append(vig)
#	vig.getKey()
#	print(vig.key)
#	cipher = vig.getTranslatedMessage()
#	print(cipher)
	
#if __name__ == '__main__':
#  main()
