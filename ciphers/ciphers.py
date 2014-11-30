import caesar, substitution, transposition, vigenere, affine

class CipherToolbox:
	def __init__(self):
		#toolbox
		self.tools = []
	def getMode(self):
		while True:
			print('Do you wish to encrypt or decrypt a message?')
			self.mode = raw_input().lower()
			if self.mode in 'encrypt e decrypt d'.split():
				return self.mode
			else:
				print('Enter either "encrypt" or "e" or "decrypt" or "d".')
	def getMessage(self):
		print('Enter your message:')
		self.message = raw_input()
		return self.message
	def getCipher(self):
		while True:
			print('Do you want to use the Caesar, Substitution, Transposition, Vigenere, or Affine cipher?')
			type = raw_input().lower()
			if type[0] == 'c':
				print('You have selected the Caesar Cipher.')
				self.current = 'c'
				break
			elif type[0] == 's':
				print('You have selected the Substitution Cipher.')
				self.current = 's'
				break
			elif type[0] == 't':
				print('You have selected the Transposition Cipher.')
				self.current = 't'
				break
			elif type[0] == 'v':
				print('You have selected the Vigenere Cipher.')
				self.current = 'v'
				break
			elif type[0] == 'a':
				print('You have selected the Affine Cipher.')
				self.current = 'a'
				break
			else:
				print('That is not a valid cipher.')
	def CryptoOp(self):
		if self.current == 'c':
			caes = caesar.CaesarCipherTool(self.mode,self.message)
			caes.getKey()
			result = caes.getTranslatedMessage()
			return result
		elif self.current == 's':
			subs = substitution.SubstitutionCipherTool(self.mode,self.message)
			subs.getKey()
			result = subs.getTranslatedMessage()
			return result
		elif self.current == 't':
			trans = transposition.TranspositionCipherTool(self.mode,self.message)
			trans.getKey()
			result = trans.getTranslatedMessage()
			return result
		elif self.current == 'v':
			vig = vigenere.VigenereCipherTool(self.mode,self.message)
			vig.getKey()
			result = vig.getTranslatedMessage()
			return result
		elif self.current == 'a':
			aff = affine.AffineCipherTool(self.mode,self.message)
			aff.getKey()
			result = aff.getTranslatedMessage()
			return result
		else:
			print('That is not a valid cipher.')
			self.getCipher()
def main():
	while True:
		toolbox = CipherToolbox()
		mod = toolbox.getMode()
		print(mod)
		mes = toolbox.getMessage()
		print(mes)
		toolbox.getCipher()
		result = toolbox.CryptoOp()
		print(result)
		
if __name__ == '__main__':
  main()