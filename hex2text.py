import sys

def hex_to_text(hexstring):
  return ''.join(chr(int(hexstring[i:i+2], 16)) for i in range(0, len(hexstring), 2))

print(hex_to_text(sys.argv[1]))
