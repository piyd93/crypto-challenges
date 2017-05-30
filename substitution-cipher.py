alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def main():
	message = input('Input a message to encrypt or decrypt: ')
	key = input('Input the key to encrypt or decrypt with: ')

	check_if_key_is_valid(key)

	action = input('Encrypt or decrypt?')

	if action == ('encrypt' or 'Encrypt' or 'e'):
		print(encrypt_message(message, key))
	elif action == ('decrypt' or 'Decrypt' or 'd'):
		print(decrypt_message(message, key))

def check_if_key_is_valid(key):
	key_list = list(key).sort()
	letter_list = list(alphabet).sort()
	if key_list != letter_list:
	  sys.exit('Error in key!')

def encrypt_message(message, key):
	encrypted_message = ''
	for symbol in message:
		if symbol.upper() in alphabet:
			symbol_index = alphabet.find(symbol.upper())
			if symbol.isupper():
				encrypted_message += key[symbol_index].upper()
			else:
				encrypted_message += key[symbol_index].lower()
		else:
			encrypted_message += symbol
	return encrypted_message

def decrypt_message(message, key):
	decrypted_message = ''
	for symbol in message:
		if symbol.upper() in alphabet:
			symbol_index = key.find(symbol.upper())
			if symbol.isupper():
				decrypted_message += alphabet[symbol_index].upper()
			else:
				decrypted_message += alphabet[symbol_index].lower()
		else:
			decrypted_message += symbol
	return decrypted_message

if __name__=='__main__':
	main()

