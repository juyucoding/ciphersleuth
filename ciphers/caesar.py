import math
import random
import os
import wsgiref.handlers
#from google.appengine.ext import webapp
#from google.appengine.ext.webapp import util
#from google.appengine.ext.webapp import template
#from google.appengine.ext import db
#from util.sessions import Session
import json
#import cryptomath
import sys

#Sourced from http://inventwithpython.com/cipher.py
class CipherToolbox:
	def __init__(self):
		#toolbox
		self.tools = []
	def getMode(self):
		while True:
			print('Do you wish to encrypt or decrypt a message?')
			mode = raw_input().lower()
			if mode in 'encrypt e decrypt d'.split():
				return mode
			else:
				print('Enter either "encrypt" or "e" or "decrypt" or "d".')
	def getMessage(self):
		print('Enter your message:')
		return raw_input()
class CaesarCipherTool:
	# Caesar Cipher
	def __init__(self, mode, message):
		self.mode = mode
		self.message = message
		self.name = 'caesar'
	MAX_KEY_SIZE = 26
	key = 0
	def getKey(self):
		while True:
			print('Enter the key number (1-%s)' % (self.MAX_KEY_SIZE))
			key = int(raw_input())
			if (key >= 1 and key <= self.MAX_KEY_SIZE):
				self.key = key
				return key
	def getTranslatedMessage(self):
		if self.mode[0] == 'd':
			self.key = -self.key
		translated = ''
		for symbol in self.message:
			if symbol.isalpha():
				num = ord(symbol)
				num += self.key
				if symbol.isupper():
					if num > ord('Z'):
						num -= 26
					elif num < ord('A'):
						num += 26
				elif symbol.islower():
					if num > ord('z'):
						num -= 26
					elif num < ord('a'):
						num += 26
				translated += chr(num)
			else:
				translated += symbol
		return translated
def main():
	toolbox = CipherToolbox()
	mod = toolbox.getMode()
	print(mod)
	mes = toolbox.getMessage()
	print(mes)
	caesar = CaesarCipherTool(mod,mes)
	toolbox.tools.append(caesar)
	caesar.getKey()
	print(caesar.key)
	cipher = caesar.getTranslatedMessage()
	print(cipher)
	
if __name__ == '__main__':
  main()