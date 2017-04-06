import base64
import binascii

hex_one = input('Enter the first buffer to xor.')
hex_two = input('Enter the second buffer to xor.')

bin_one = hex_one.decode("hex")
bin_two = hex_two.decode("hex")

xored = "".join(chr(ord(a) ^ ord(b)) for a,b in zip(bin_one, bin_two))

hexored = xored.encode("hex")

print hexored


