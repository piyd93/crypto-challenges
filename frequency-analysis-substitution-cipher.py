alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
english_order = 'ETAOINSHRDLCUMWFGYPBVKJXQZ'
english_letter_frequencies = {'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97, 'N': 6.75, 'S': 6.33, 'H': 6.09, 'R': 5.99, 'D': 4.25, 'L': 4.03, 'C': 2.78,
    'U': 2.76, 'M': 2.41, 'W': 2.36, 'F': 2.23, 'G': 2.02, 'Y': 1.97, 'P': 1.93, 'B': 1.29, 'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15, 'Q': 0.10, 'Z': 0.07}


def get_letter_count(englishtext):
  letter_count = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0, 'I': 0, 'J': 0, 'K': 0, 'L': 0,
      'M': 0, 'N': 0, 'O': 0, 'P': 0, 'Q': 0, 'R': 0, 'S': 0, 'T': 0, 'U': 0, 'V': 0, 'W': 0, 'X': 0, 'Y': 0, 'Z': 0}
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

def frequency_analysis_substitution_cipher(message):
  current_max_match = 0
  decrypted = ''
  for letter in alphabet:
    if get_match_score(message) > current_max_match: