import caesar, substitution, transposition, vigenere, affine

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

def main():
	toolbox = CipherToolbox()
	mod = toolbox.getMode()
	print(mod)
	mes = toolbox.getMessage()
	print(mes)
	trans = transposition.TranspositionCipherTool(mod,mes)
	toolbox.tools.append(trans)
	trans.getKey()
	print(trans.key)
	cipher = trans.getTranslatedMessage()
	print(cipher)
	
if __name__ == '__main__':
  main()