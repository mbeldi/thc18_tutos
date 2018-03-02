#### Write-up

**AES-CBC**

AES est un chiffrement par bloc, ce qui signifie que le texte en clair est divisé en blocs: chaque bloc est codé avec une clé de chiffrement d'une longueur égale (128, 192 ou 256 bits dans le cas d'AES). 

En soi, un chiffrement par bloc ne convient que pour la transmission sécurisée d'un bloc. Donc, afin de coder de plus grandes quantités de données, divers modes de fonctionnement ont été introduits. CBC (Cipher Block Chaining) est l'un de ces modes.

![CBC](https://upload.wikimedia.org/wikipedia/commons/thumb/4/42/Schema_CBC.svg/1482px-Schema_CBC.svg.png)

Comme le montre la figure, pour chiffrer un bloc en mode CBC, on effectue un "ou exclusif" (XOR) entre le texte en clair de chaque bloc et le texte chiffré du bloc précédent (ou le vecteur d'initialisation IV pour le premier bloc), puis codé avec un algorithme choisi (AES dans notre cas). 

CBC est largement utilisé, mais à cause de ses propriétés, il est vulnérable aux attaques de retournement d'octets (byte-flipping attacks).

**Byte-flipping attack**

Cela veut dire que lorsqu'on change un octet dans le texte chiffré d'un bloc, l'octet dans la même position du texte suivant du bloc suivant est modifié à cause de l'opération XOR. Voyons cela:

```
$ echo "Change cet octet: M" | openssl aes-128-cbc -K
AABBAABBAABBAABBAABBAABBAABBAABB -iv AABBAABBAABBAABBAABBAABBAABBAABB > text
$ xxd text
00000000: 48a3 2855 27e0 53cd 7f7a 6692 e7bf d0fb  H.(U'.S..zf.....
00000010: a83b 4e75 ee26 2d72 d8ba 3365 857f ba6e  .;Nu.&-r..3e...n
```

La taille de bloc de AES-128 est de 16 octets, ce qui signifie que la lettre "M" que nous devons changer tombe dans le troisième octet du second bloc:
```
48 A3 28 55 27 E0 53 CD 7F 7A 66 92 E7 BF D0 FB
C  h  a  n  g  e     c  e  t     o  c  t  e  t 
A8 3B 4E 75 EE 26 2D 72 D8 BA 33 65 85 7F BA 6E
:     M
```


Comme décrit précédemment, pour inverser un octet du texte en clair d'un bloc, nous devons inverser l'octet correspondant du texte chiffré du bloc précédent, ce qui signifie que changer 28 (troisième octet du premier bloc) changera M dans le message codé. Pour changer de M à A nous aurons besoin de XOR 28 avec (M XOR A), alors découvrons la valeur avec Python:
```
>>> hex(0x28 ^ ord("M") ^ ord("A"))
'0x24'
```

Changeons notre texte chiffré pour modifier de 28 à 24, décodons-le et voyons s'il a fonctionné:
```
$ printf '\x24' | dd of=message bs=1 seek=2 count=1 conv=notrunc &> /dev/null
$ xxd message
00000000: 48a3 2455 27e0 53cd 7f7a 6692 e7bf d0fb  H.$U'.S..zf.....
00000010: a83b 4e75 ee26 2d72 d8ba 3365 857f ba6e  .;Nu.&-r..3e...n
$ cat message | openssl aes-128-cbc -d -K AABBAABBAABBAABBAABBAABBAABBAABB
-iv AABBAABBAABBAABBAABBAABBAABBAABB

sD4ɾ*@C: A
```

On peut remarquer que que le M a changé en A comme prévu, donc l'attaque a réussi. 
Cependant, le premier bloc est maintenant brouillé depuis que nous avons changé son texte chiffré, et ce fait rend l'attaque presque irréalisable en dehors de la portée de la curiosité académique. En plus, cette attaque n'est réalisable que sur un seul bloc.
On pourrait modifier le premier bloc seulement si l'IV est connu et peut être modifié.

**Solution**

Une solution de ce challenge peut être:

```
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
print "Received: "+msg

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
```

Ce code fait exactement ce qu'on a décrit dans l'explication du byte-flipping attack. 
Il change les 15 premiers octets du premier bloc du chiffré afin de changer ainsi les 15 premiers octets du deuxième bloc du clair qui correspondent à `18;admin=false;`.
Et pour faire cela, il remplace l'octet de la i ème position du deuxième bloc du chiffré par son ancienne valeur xor l'ancienne lettre xor la nouvelle lettre. (Ceci est expliqué précédemment).

On trouve le flag `THC18{TheB1rdeCh4nges!}`
