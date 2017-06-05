import binascii
import codecs
import itertools
import math

from Crypto.Cipher import AES

def xorbytes(a,b):
  return bytes(x^y for x,y in zip(a,b))

def hex_to_text(hexstring):
  return ''.join(chr(int(hexstring[i:i+2], 16)) for i in range(0, len(hexstring), 2))

def hextobase64(hexstring):
  binarystring = binascii.unhexlify(hexstring)
  return binascii.b2a_base64(binarystring)

def base64tobytes(base64str):
  return binascii.a2b_base64(base64str)

def hexXOR(hex_one, hex_two):
  return hex(hex_one ^ hex_two)

alphabet = ' ABCDEFGHIJKLMNOPQRSTUVWXYZ:'
english_order = ' ETAOINSHRDLCUMWFGYPBVKJXQZ:'
english_letter_frequencies = {'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97, 'N': 6.75, 'S': 6.33, 'H': 6.09, 'R': 5.99, 'D': 4.25, 'L': 4.03, 'C': 2.78,
    'U': 2.76, 'M': 2.41, 'W': 2.36, 'F': 2.23, 'G': 2.02, 'Y': 1.97, 'P': 1.93, 'B': 1.29, 'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15, 'Q': 0.10, 'Z': 0.07}


def get_letter_count(englishtext):
  letter_count = {' ': 0, 'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0, 'I': 0, 'J': 0, 'K': 0, 'L': 0,
      'M': 0, 'N': 0, 'O': 0, 'P': 0, 'Q': 0, 'R': 0, 'S': 0, 'T': 0, 'U': 0, 'V': 0, 'W': 0, 'X': 0, 'Y': 0, 'Z': 0, ':': 0}
  for letter in englishtext.upper():
  	if letter in alphabet:
  	  letter_count[letter] += 1
  return letter_count


def get_frequency_order(message):
  letter_count_dict = get_letter_count(message)
  frequency_order = ''

  for letter in sorted(letter_count_dict, key=letter_count_dict.get, reverse=True):
  	frequency_order += letter
  return frequency_order


def get_match_score(message):
  # return number of matches the message has when its frequency order is
  # compared to the english frequency order
  message_order = get_frequency_order(message)
  matches = 0
  # check 6 most frequent letters
  for letter in english_order[:6]:
  	if letter in message_order[:6]:
  	  matches += 1
  # check 6 least frequent letters
  for letter in english_order[-6:]:
  	if letter in message_order[-6:]:
  	  matches += 1

  return matches


def crack_single_byte_xor(hex_message):
  key = ''
  decrypted = ''
  current_max_match = 0
  bytes_message = bytes.fromhex(hex_message)
  for letter in alphabet:
    letter_string = hex(ord(letter))[2:]*(len(hex_message)+1//2)
    bytes_letter_string = bytes.fromhex(letter_string)
    xored = xorbytes(bytes_letter_string, bytes_message)
    test_message = xored.decode()
    print(test_message)
    if get_match_score(test_message) > current_max_match:
      key = letter
      decrypted = test_message
      current_max_match = get_match_score(test_message)
  print('key = ' + letter)
  return decrypted

def crack_single_byte_xor_bytes(bytes_message):
  key = ''
  decrypted = ''
  current_max_match = 0
  for letter in alphabet:
    letter_string = hex(ord(letter))[2:]*(len(bytes_message)+1//2)
    bytes_letter_string = bytes.fromhex(letter_string)
    xored = xorbytes(bytes_letter_string, bytes_message)
    test_message = xored.decode()
    if get_match_score(test_message) > current_max_match:
      key = letter
      decrypted = test_message
      current_max_match = get_match_score(test_message)
  #print(decrypted)
  return key

def repeating_key_xor(message, key):
  bytes_message = message.encode()
  key_string = key*(len(message))
  bytes_key_string = key_string.encode()
  xored = xorbytes(bytes_message, bytes_key_string)
  return xored

def repeating_key_xor_bytes(bytes_message, key):
  key_string = key*(len(bytes_message))
  bytes_key_string = key_string.encode()
  xored = xorbytes(bytes_message, bytes_key_string)
  return xored

def compute_num_differing_bits(str1, str2):
  assert len(str1) == len(str2)
  return sum([bin(str1[i] ^ str2[i]).count('1') for i in range(len(str1))])

def crack_repeating_key_xor(message):
  # thanks to http://www.cypher.codes/2017/04/21/cryptopals-challenge-set-1.html for helping
  # me get unstuck with this one
  KEYSIZE = 2
  min_edit_distance = math.inf
  normalized = []
  for size in range(2, 40):
    first = message[: size]
    second = message[size: size*2]
    third = message[size*2: size*3]
    fourth = message[size*3: size*4]
    normalized.append((size,float(compute_num_differing_bits(first,second)
      +compute_num_differing_bits(second,third)+compute_num_differing_bits(third,fourth))/(size*3)))
    
  normalized = sorted(normalized, key=lambda x:x[1])

  # for some reason normalized[2] holds the correct answer, just going to go with that for now
  for i in range(0, 3):
    KEYSIZE = normalized[i];
    # break ciphertext into blocks of KEYSIZE length
    blocks = [message[i:i+KEYSIZE[0]] for i in range(0, len(message), KEYSIZE[0])]
    # get all the characters at place 0 through keysize (zip lengthwise, rotate)
    transposedBlocks = list(itertools.zip_longest(*blocks, fillvalue=0))

    # solve each block
    key = ''
    for x in transposedBlocks:
      key+=crack_single_byte_xor_bytes(bytes(x))
  return key


# challenge8

texts = []
max_reps = 0
ecb = None
for text in list(open("8.txt", 'rb')):
  # create a dictionary to store number of times a block is repeated
  repetitions_dictionary = {}

  # divide text into blocks of 16
  blocks = [text[i:i+16] for i in range(0, len(text), 16)]

  # for each block, store it in the dictionary/increment number of repetitions if it's already in the dictionary
  for block in blocks:
    if(block in repetitions_dictionary):
      repetitions_dictionary[block] += 1
    else:
      repetitions_dictionary[block] = 0

  # sum up the number of repetitions for this piece of text
  num_reps = sum(repetitions_dictionary.values())

  if num_reps > max_reps:
    max_reps = num_reps
    ecb = text

print(max_reps)
print(ecb)

# ----------end challenge8-------------------

# challenge7
#file = codecs.decode(open('7.txt', 'rb').read(), 'base64')
#print(AES.new("YELLOW SUBMARINE", AES.MODE_ECB).decrypt(file))

# ----------end challenge7-------------------

# challenge6
# bfile = open('6.txt', 'rb').read()
# bfile = codecs.decode(bfile, 'base64')

# key = crack_repeating_key_xor(bfile)
# print("key returned by crack")
# print(key)

# decoded = repeating_key_xor_bytes(bfile, key).decode()
# print(decoded)

# ----------end challenge6-------------------

# test hamming distance :)
# str1 = input("enter str1").encode('utf-8')
# str2 = input("enter str2").encode('utf-8')
# print(str1)
# print(str2)
# print(compute_num_differing_bits(str1, str2))

# ----------end hammingdistance--------------

# challenge5
# message = input("enter message to encrypt using repeating key xor: ")
# key = input("enter key for repeating key xor: ")
# encrypted = repeating_key_xor(message, key)
# print(encrypted)
# print(encrypted.hex())

# ----------end challenge5-------------------

# challenge3
# message = input('enter string to decode (single-byte xor cipher): ')
# print(crack_single_byte_xor(message))

# ----------end challenge3-------------------

# challenge2
# one = input('Enter the first buffer to xor.')
# two = input('Enter the second buffer to xor.')
# print(hexXOR(int(one, 16), int(two, 16)))

# ----------end challenge2-------------------

# challenge 1
# hexstring = input('Enter the hex number to base64 encode.')
# print(hextobase64(hexstring))


# ----------end challenge1-------------------

