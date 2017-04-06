import binascii

hexstring = input('Enter the hex number to base64 encode.')

binarystring = binascii.unhexlify(hexstring)

print binascii.b2a_base64(binarystring)


