import math
import random
import os
import wsgiref.handlers
import json
import sys

class TranspositionCipherTool:
# Transposition Cipher Encryption
# http://inventwithpython.com/hacking (BSD Licensed)
# made some modifications to source
	def __init__(self, mode, message,maxlen):
		self.mode = mode
		self.message = message
		self.name = 'transposition'
		self.maxlen=maxlen
		#self.MAX_KEY_SIZE = len(self.message)
	key = 0
	def display(self):
		return self.mode + " " +self.message + " " + self.name+" "+str(self.maxlen)
	def getlen(self):
		return self.MAX_KEY_SIZE
	def storekey(self,key):
		self.key=key
	def getKey(self):
		while True:
			print('Enter the key number (1-%s)' % (self.MAX_KEY_SIZE))
			key = int(raw_input())
			if (key >= 1 and key <= self.MAX_KEY_SIZE):
				self.key = key
				return key
	def getTranslatedMessage(self):
		if self.mode[0] == 'd':
			# The transposition decrypt function will simulate the "columns" and
			# "rows" of the grid that the plaintext is written on by using a list
			# of strings. First, we need to calculate a few values.
			# The number of "columns" in our transposition grid:
			numOfColumns = int(math.ceil(len(self.message) / self.key))+1
			# numOfColumns = int(numOfColumns)
			# The number of "rows" in our grid will need:
			numOfRows = self.key
			# The number of "shaded boxes" in the last "column" of the grid:
			numOfShadedBoxes = (numOfColumns * numOfRows) - len(self.message)

			# Each string in plaintext represents a column in the grid.
			plaintext = [''] * numOfColumns

			# The col and row variables point to where in the grid the next
			# character in the encrypted message will go.
			col = 0
			row = 0

			for symbol in self.message:
				plaintext[col] += symbol
				col += 1 # point to next column

				# If there are no more columns OR we're at a shaded box, go back to
				# the first column and the next row.
				if (col == numOfColumns) or ((col == numOfColumns - 1) and (row >= numOfRows - numOfShadedBoxes)):
					col = 0
					row += 1
			return ''.join(plaintext)
		else:
			# Each string in ciphertext represents a column in the grid.
			ciphertext = [''] * self.key
			# Loop through each column in ciphertext.
			for col in range(self.key):
				pointer = col
				
				# Keep looping until pointer goes past the length of the message.
				while pointer < len(self.message):
					# Place the character at pointer in message at the end of the
					# current column in the ciphertext list.
					ciphertext[col] += self.message[pointer]
					
					# move pointer over
					pointer += self.key
		# Convert the ciphertext list into a single string value and return it.
			return ''.join(ciphertext)
#def main():
#	toolbox = CipherToolbox()
#	mod = toolbox.getMode()
#	print(mod)
#	mes = toolbox.getMessage()
#	print(mes)
#	trans = TranspositionCipherTool(mod,mes)
#	toolbox.tools.append(trans)
#	trans.getKey()
#	print(trans.key)
#	cipher = trans.getTranslatedMessage()
#	print(cipher)
	
#if __name__ == '__main__':
#  main()
