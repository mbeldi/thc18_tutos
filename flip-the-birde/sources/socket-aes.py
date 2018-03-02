#!/usr/bin/env python
# coding: utf-8 

import socket
import threading
import base64
import hashlib
import random
from Crypto.Cipher import AES

## CLIENT THREAD ##
class ClientThread(threading.Thread):

    def __init__(self, ip, port, clientsocket):

        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.clientsocket = clientsocket
        print("\t[+] Creating new thread %s:%s" % (self.ip, self.port, ))

    def run(self): 
        print("\t[+] Connecting %s:%s" % (self.ip, self.port, ))
        self.run_chall()
        print("\t[+] Disconnecting %s:%s" % (self.ip, self.port, ))
        self.clientsocket.close()

    def run_chall(self):
        plaintext = 'localhost:'+str(nb_rand)+'018;admin=false;'
        ciphertext_b64 = aes.encrypt(plaintext)
        to_send = welcome_msg
        to_send += 'Plaintext: '+plaintext
        to_send += '\nCiphertext: '+ciphertext_b64
        to_send += '\nModified ciphertext: '
        self.clientsocket.send(to_send)
        rcv = self.clientsocket.recv(512)
        print("\t[+] Received from %s:%s : %s" % (self.ip, self.port, rcv, ))
        try:
            ans = aes.decrypt(rcv.strip('\n'))
        except:
            self.clientsocket.send('Wrong format!\n')
            self.clientsocket.close()
            exit()
        ans = ans[16:]

        if 'admin=true;' in ans:
            self.clientsocket.send(flag)
        else:
            if 'admin=true' in ans:
                self.clientsocket.send('Ops, you forgot one byte.\n')
            else:
                self.clientsocket.send('Incorrect.\n')


## AES CIPHER ##
class AESCipher(object):

    def __init__(self, key): 
        self.bs = AES.block_size
        self.key = key.encode()
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        raw = self._pad(raw)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc))

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]

## MAIN ##   

welcome_msg = '\n    Flip the Birde\n'
welcome_msg += '======================\n\n'
welcome_msg += 'Message is encrypted with AES-CBC with unknown key and IV.\n'
welcome_msg += 'Your task is to modify the ciphertext!\n'
welcome_msg += 'To bypass the authentication, the plaintext must contain \'admin=true;\'.\n'

key = 'Anything_U_Want'
iv = '0000000000000a0a'
aes = AESCipher(key)
flag = 'THC18{TheB1rdeCh4nges!}'

tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind(("",41222))

while True:
    tcpsock.listen(10)
    print( "[*] Listening...")
    (clientsocket, (ip, port)) = tcpsock.accept()
    cl_thread = ClientThread(ip, port, clientsocket)
    nb_rand = random.randint(11111, 88888)
    cl_thread.start()
