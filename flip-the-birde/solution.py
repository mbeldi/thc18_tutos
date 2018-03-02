import base64
import hashlib
import binascii
from Crypto import Random
from Crypto.Cipher import AES
from pwn import *

if(len(sys.argv) < 2):
    print "Usage: python %s %s" % (sys.argv[0], '<port_number>')
    exit();

con = remote('localhost', sys.argv[1])
msg = con.recvline_contains('Ciphertext: ')
msg = msg[12:]
msg = msg.strip('\n')
msg = msg.strip('\t')

# 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6
# l o c a l h o s t : x x x x x ;
# 1 8 ; a d m i n = f a l s e ;

#convert to/from base64
arr = ' '.join(x.encode('hex') for x in base64.b64decode(msg))
print "Received: "+arr

arr = arr.split(' ')
ori = ['f', 'a', 'l', 's', 'e']
new = ['t', 'r', 'u', 'e', ';']
for i in range(0, 5):
    arr[9+i] = hex(int(arr[9+i], 16) ^ ord(ori[i]) ^ ord(new[i]))
    arr[9+i] = arr[9+i].replace('0x','')

modif = ''.join(v for v in arr)
modif = binascii.unhexlify(modif.strip())
modif = base64.b64encode(modif)
print "Send: "+modif
con.recv()
con.sendline(modif)
print con.recv()

