import math
import random
import os
import wsgiref.handlers
from google.appengine.ext import webapp
#from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from util.sessions import Session
import json
import cryptomath
import sys

#Sourced from http://inventwithpython.com/cipher.py
class CipherToolbox:
	def getMode():
		while True:
			print('Do you wish to encrypt or decrypt a message?')
			mode = input().lower()
			if mode in 'encrypt e decrypt d'.split():
				return mode
			else:
				print('Enter either "encrypt" or "e" or "decrypt" or "d".')
	def getMessage():
		print('Enter your message:')
		return input()
	
class CaesarCipherTool(mode, message):
	# Caesar Cipher
	MAX_KEY_SIZE = 26
	def getKey():
		key = 0
		while True:
			print('Enter the key number (1-%s)' % (MAX_KEY_SIZE))
			key = int(input())
			if (key >= 1 and key <= MAX_KEY_SIZE):
				return key
	def getTranslatedMessage(mode, message, key):
		if mode[0] == 'd':
			key = -key
		translated = ''
		for symbol in message:
			if symbol.isalpha():
				num = ord(symbol)
				num += key
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
	mode = CipherToolbox.getMode()
	message = CipherToolbox.getMessage()
	key = getKey()
	#print('Your translated text is:')
	#print(getTranslatedMessage(mode, message, key))
	
class SubstitutionCipherTool(mode, message):
# Simple Substitution Cipher
# http://inventwithpython.com/hacking (BSD Licensed)
# made some modifications to source
	LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
	def checkValidKey(key):
	    keyList = list(key)
	    lettersList = list(LETTERS)
	    keyList.sort()
	    lettersList.sort()
	    if keyList != lettersList:
	        print('This key is invalid.')
			return False
		else:
			return True
	def getKey():
		print('Input the 26-letter string of characters to use as a key:')
		key = input()
		while checkValidKey(key) != True:
			print('That key is invalid. Please enter a new one:')
			key = input()
		return key
	def getTranslatedMessage(mode, message, key):
		translated = ''
		charsA = LETTERS
		charsB = key
		if mode[0] == 'd':
			charsA, charsB = charsB, charsA
		
		# loop through each symbol in the message
		for symbol in message:
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
	mode = CipherToolbox.getMode()
	message = CipherToolbox.getMessage()
	key = getKey()
	#print('Your translated text is:')
	#print(getTranslatedMessage(mode, message, key))

class TranspositionCipherTool(mode, message):
# Transposition Cipher Encryption
# http://inventwithpython.com/hacking (BSD Licensed)
	MAX_KEY_SIZE = len(message)
	def getKey():
		key = 0
		while True:
			print('Enter the key number (1-%s)' % (MAX_KEY_SIZE))
			key = int(input())
			if (key >= 1 and key <= MAX_KEY_SIZE):
				return key				
	def getTranslatedMessage(mode, message, key):
		if mode[0] == 'd':
			# The transposition decrypt function will simulate the "columns" and
			# "rows" of the grid that the plaintext is written on by using a list
			# of strings. First, we need to calculate a few values.
			# The number of "columns" in our transposition grid:
			numOfColumns = math.ceil(len(message) / key)
			# The number of "rows" in our grid will need:
			numOfRows = key
			# The number of "shaded boxes" in the last "column" of the grid:
			numOfShadedBoxes = (numOfColumns * numOfRows) - len(message)

			# Each string in plaintext represents a column in the grid.
			plaintext = [''] * numOfColumns

			# The col and row variables point to where in the grid the next
			# character in the encrypted message will go.
			col = 0
			row = 0

			for symbol in message:
				plaintext[col] += symbol
				col += 1 # point to next column

				# If there are no more columns OR we're at a shaded box, go back to
				# the first column and the next row.
				if (col == numOfColumns) or (col == numOfColumns - 1 and row >= numOfRows - numOfShadedBoxes):
					col = 0
					row += 1
			return ''.join(plaintext)
		else:
			# Each string in ciphertext represents a column in the grid.
			ciphertext = [''] * key
			# Loop through each column in ciphertext.
			for col in range(key):
				pointer = col
				
				# Keep looping until pointer goes past the length of the message.
				while pointer < len(message):
					# Place the character at pointer in message at the end of the
					# current column in the ciphertext list.
					ciphertext[col] += message[pointer]
					
					# move pointer over
					pointer += key
		# Convert the ciphertext list into a single string value and return it.
			return ''.join(ciphertext)
	mode = CipherToolbox.getMode()
	message = CipherToolbox.getMessage()
	key = getKey()
	#print(ciphertext + '|')
	
class AffineCipherTool(mode, message):
	# Affine Cipher
	# http://inventwithpython.com/hacking (BSD Licensed)
	SYMBOLS = """ !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\] ^_`abcdefghijklmnopqrstuvwxyz{|}~""" # note the space at the front
	def getRandomKey():
		while True:
			keyA = random.randint(2, len(SYMBOLS))
			keyB = random.randint(2, len(SYMBOLS))
			if cryptomath.gcd(keyA, len(SYMBOLS)) == 1:
				return keyA * len(SYMBOLS) + keyB
	def getKey():
		key = 0
		while True:
			print('Enter the key number:')
			key = int(input())
			return key
	def getKeyParts(key):
		keyA = key // len(SYMBOLS)
		keyB = key % len(SYMBOLS)
		return (keyA, keyB)
	def checkKey(keyA, keyB, mode):
		if keyA == 1 and mode == 'encrypt':
			sys.exit('The affine cipher becomes incredibly weak when key A is set to 1. Choose a different key.')
		if keyB == 0 and mode == 'encrypt':
			sys.exit('The affine cipher becomes incredibly weak when key B is set to 0. Choose a different key.')
		if keyA < 0 or keyB < 0 or keyB > len(SYMBOLS) - 1:
			sys.exit('Key A must be greater than 0 and Key B must be between 0 and %s.' % (len(SYMBOLS) - 1))
		if cryptomath.gcd(keyA, len(SYMBOLS)) != 1:
			sys.exit('Key A (%s) and the symbol set size (%s) are not relatively prime. Choose a different key.' % (keyA, len(SYMBOLS)))
	def getTranslatedMessage(mode, message, key):
		if mode[0] == 'd':
			keyA, keyB = getKeyParts(key)
			checkKeys(keyA, keyB, 'decrypt')
			plaintext = ''
			modInverseOfKeyA = cryptomath.findModInverse(keyA, len(SYMBOLS))

			for symbol in message:
				if symbol in SYMBOLS:
				# decrypt this symbol
					symIndex = SYMBOLS.find(symbol)
					plaintext += SYMBOLS[(symIndex - keyB) * modInverseOfKeyA % len(SYMBOLS)]
				else:
					plaintext += symbol # just append this symbol undecrypted
				return plaintext
		else:
			keyA, keyB = getKeyParts(key)
			checkKeys(keyA, keyB, 'encrypt')
			ciphertext = ''
			for symbol in message:
				if symbol in SYMBOLS:
				# encrypt this symbol
					symIndex = SYMBOLS.find(symbol)
					ciphertext += SYMBOLS[(symIndex * keyA + keyB) % len(SYMBOLS)]
				else:
					ciphertext += symbol # just append this symbol unencrypted
			return ciphertext
	mode = CipherToolbox.getMode()
	message = CipherToolbox.getMessage()
	key = getKey()
	#print('Your translated text is:')
	#print(getTranslatedMessage(mode, message, key))
	
class VigenereCipherTool(mode, message):
	# Vigenere Cipher (Polyalphabetic Substitution Cipher)
	# http://inventwithpython.com/hacking (BSD Licensed)
	LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
	def checkValidKey(key):
	    keyList = list(key)
	    lettersList = list(LETTERS)
	    keyList.sort()
	    lettersList.sort()
	    if keyList != lettersList:
	        print('This key is invalid.')
			return False
		else:
			return True
	def getKey():
		print('Input a string of letters to use as a key:')
		key = input()
		while checkValidKey(key) != True:
			print('That key is invalid. Please enter a new one:')
			key = input()
		return key	
	def getTranslatedMessage(mode, message, key):
		translated = [] # stores the encrypted/decrypted message string
		keyIndex = 0
		key = key.upper()

		for symbol in message: # loop through each character in message
			num = LETTERS.find(symbol.upper())
			if num != -1: # -1 means symbol.upper() was not found in LETTERS
				if mode[0] == 'e':
					num += LETTERS.find(key[keyIndex]) # add if encrypting
				elif mode[0] == 'd':
					num -= LETTERS.find(key[keyIndex]) # subtract if decrypting
	
				num %= len(LETTERS) # handle the potential wrap-around
	
				# add the encrypted/decrypted symbol to the end of translated.
				if symbol.isupper():
					translated.append(LETTERS[num])
				elif symbol.islower():
					translated.append(LETTERS[num].lower())

				keyIndex += 1 # move to the next letter in the key
				if keyIndex == len(key):
					keyIndex = 0
			else:
				# The symbol was not in LETTERS, so add it to translated as is.
				translated.append(symbol)

		return ''.join(translated)
	mode = CipherToolbox.getMode()
	message = CipherToolbox.getMessage()
	key = getKey()
	#print('Your translated text is:')
	#print(getTranslatedMessage(mode, message, key))	

	
class RSACipherTool(mode,message):
	# RSA Cipher
	# http://inventwithpython.com/hacking (BSD Licensed)
	# IMPORTANT: The block size MUST be less than or equal to the key size!
	# (Note: The block size is in bytes, the key size is in bits. There
	# are 8 bits in 1 byte.)
	DEFAULT_BLOCK_SIZE = 128 # 128 bytes
	BYTE_SIZE = 256 # One byte has 256 different values.
	# create a public/private keypair with 1024 bit keys
	def genRSAKeys():
		keySize = 1024
		# Creates a public/private key pair with keys that are keySize bits in
		#size. This function may take a while to run.
		# Step 1: Create two prime numbers, p and q. Calculate n = p * q.
		print('Generating p prime...')
		p = rabinMiller.generateLargePrime(keySize)
		print('Generating q prime...')
		q = rabinMiller.generateLargePrime(keySize)
		n = p * q
		# Step 2: Create a number e that is relatively prime to (p-1)*(q-1).
		print('Generating e that is relatively prime to (p-1)*(q-1)...')
		while True:
			# Keep trying random numbers for e until one is valid.
			e = random.randrange(2 ** (keySize - 1), 2 ** (keySize))
			if cryptomath.gcd(e, (p - 1) * (q - 1)) == 1:
			break
		# Step 3: Calculate d, the mod inverse of e.
		print('Calculating d that is mod inverse of e...')
		d = cryptomath.findModInverse(e, (p - 1) * (q - 1))
		publicKey = (n, e)
		privateKey = (n, d)
		print('Public key:', publicKey)
		print('Private key:', privateKey)
		#Save keys to GameDataStore for particular character
	def getPubKey(name):
		#fetch Key from GameDataStore for particular person
		return keya
	def getPrivKey(name):
		#fetch Key from GameDataStore for particular person
		return keyb
	def getBlocksFromText(message, blockSize=DEFAULT_BLOCK_SIZE):
		# Converts a string message to a list of block integers. Each integer
		# represents 128 (or whatever blockSize is set to) string characters.
	
		messageBytes = message.encode('ascii') # convert the string to bytes
 
		blockInts = []
		for blockStart in range(0, len(messageBytes), blockSize):
			# Calculate the block integer for this block of text
			blockInt = 0
			for i in range(blockStart, min(blockStart + blockSize, len(messageBytes))):
				blockInt += messageBytes[i] * (BYTE_SIZE ** (i % blockSize))
		blockInts.append(blockInt)
		return blockInts
	def getTextFromBlocks(blockInts, messageLength, blockSize=DEFAULT_BLOCK_SIZE):
		# Converts a list of block integers to the original message string.
		# The original message length is needed to properly convert the last
		# block integer.
		message = []
		for blockInt in blockInts:
			blockMessage = []
		for i in range(blockSize - 1, -1, -1):
			if len(message) + i < messageLength:
			# Decode the message string for the 128 (or whatever
			# blockSize is set to) characters from this block integer.
				asciiNumber = blockInt // (BYTE_SIZE ** i)
				blockInt = blockInt % (BYTE_SIZE ** i)
				blockMessage.insert(0, chr(asciiNumber))
				message.extend(blockMessage)
		return ''.join(message)
	def getTranslatedMessage(mode, message, name, messagelength):
		if mode[0] == 'e':
			return encryptMessage(message, name)
		else:
			return decryptMessage(message, name, messagelength)
	def encryptMessage(message, name):
		n, e = getPubKey(name)
		# Encrypt the message
		blockSize = DEFAULT_BLOCK_SIZE
		encryptedBlocks = []
		for block in getBlocksFromText(message, blockSize):
			# ciphertext = plaintext ^ e mod n
			encryptedBlocks.append(pow(block, e, n))
		# Convert the large int values to one string value.
		for i in range(len(encryptedBlocks)):
			encryptedBlocks[i] = str(encryptedBlocks[i])
			encryptedContent = ','.join(encryptedBlocks)
		# Write out the encrypted string and length of original message to the database. 
		return encryptedContent
	def decryptMessage(message, name, messagelength):
		# Using a key from a key file, read an encrypted message from a file
		# and then decrypt it. Returns the decrypted message string.
		n, d = getPrivKey(name)
		blockSize = DEFAULT_BLOCK_SIZE
		# Convert the encrypted message into large int values.
		encryptedBlocks = []
		encryptedMessage = message;
		for block in encryptedMessage.split(','):
			encryptedBlocks.append(int(block))
		# Decrypts a list of encrypted block ints into the original message
		# string. The original message length is required to properly decrypt
		# the last block. Be sure to pass the PRIVATE key to decrypt.
		decryptedBlocks = []
		for block in encryptedBlocks:
			# plaintext = ciphertext ^ d mod n
			decryptedBlocks.append(pow(block, d, n))
		return getTextFromBlocks(decryptedBlocks, messageLength, blockSize)
	mode = CipherToolbox.getMode()
	message = CipherToolbox.getMessage()
	#print('Your translated text is:')
	#print(getTranslatedMessage(mode, message, key))	
