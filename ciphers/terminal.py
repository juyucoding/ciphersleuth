import math
import random
import os
import wsgiref.handlers
#from google.appengine.ext import webapp
#from google.appengine.ext.webapp import util
#from google.appengine.ext.webapp import template
#from google.appengine.ext import db
#from util.sessions import Session
#import json
from django.utils import simplejson as json
import sys
import ciphers

def help():
	while True:
		print('Would you like to go to the tutorial for the Caesar cipher, Substitution cipher, Transposition cipher, Vigenere cipher, or Affine cipher? You can also type toolbox to use the ciphers.')
		type = raw_input().lower()
		if type[0] == 'c':
			print('You have selected the Caesar Cipher.')
		elif type[0] == 's':
			print('You have selected the Substitution Cipher.')
		elif type == 'transposition':
			print('You have selected the Transposition Cipher.')
		elif type[0] == 'v':
			print('You have selected the Vigenere Cipher.')
		elif type[0] == 'a':
			print('You have selected the Affine Cipher.')
		elif type == 'toolbox':
			print('You have selected to go to the toolbox')
			ciphers.toolboxMenu()
		else:
			print('That is not a valid cipher.')
def main():
	print('Welcome to the CipherSleuth toolbox!')
	print('Here, you can access the functions you need to decode the messages and move to each level.')
	print('Sometimes you will be given the key to decrypt a message, other times you might have to keep trying different keys until you get an answer that makes sense.')
	print('Would you like to go the help menu or the cipher toolbox?')
	a = raw_input().lower()
	if a[0] == 'h':
		help()
	else:
		ciphers.toolboxMenu()
	
if __name__ == '__main__':
  main()
