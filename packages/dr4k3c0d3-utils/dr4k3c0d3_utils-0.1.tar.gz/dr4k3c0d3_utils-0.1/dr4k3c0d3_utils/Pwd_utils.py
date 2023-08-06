'''
Module : Pwd-utils.py
Objectif du script : Allow to encode/decode textplain with 'key's computer dependant' or any key else you need to implement
Technologie utilisée : Crypto blowfish - platform UUID
Auteur : DrakeCode
Date création : 30/03/2021
Version : 0.1
Personnal Library : dr4k3c0d3-utils
'''

'''
Import module
Pycryptodome:    fork from pycrypto - pip install pycryptodome
'''
from Crypto.Cipher import Blowfish
from Crypto import Random

from subprocess import check_output
from struct import pack
from base64 import b64encode, b64decode

import platform as pt


class Pwd_mgt:

    def __init__(self, key=None):
        if key is None:
            self._key = self._GetUUID()
        else:
            self._key = key

    '''
    Private Functions
    '''
    def _GetUUID(self):

        ''' Return uuid from computer
            platform dependant
        '''
        if pt.system() == 'Windows' :
            cmd = 'wmic csproduct get uuid'
            uuid = str(check_output(cmd))
            pos1 = uuid.find("\\n")+2
            return uuid[pos1:-15]
        elif pt.system() == 'Linux' :
            raise "Todo for linux platform" + self._GetUUID.__name__

    '''
    Public Functions
    '''
    def encrypt(self, plaintext):
        ''' Return encrypted plaintext (string) with key
        '''
        plaintext = plaintext.encode("utf-8") # "utf-8" by default

        bs = Blowfish.block_size
        iv = Random.new().read(bs)
        cipher = Blowfish.new(self._key.encode("utf-8"), Blowfish.MODE_CBC, iv)
        
        plen = bs - divmod(len(plaintext),bs)[1]
        padding = [plen]*plen
        padding = pack('b'*plen, *padding)
        
        msg = iv + cipher.encrypt(plaintext + padding) #bytes

        encoded = b64encode(msg)
        
        return  encoded.decode('ascii') #string

    def decrypt(self, ciphertext):
        '''
            Return decypted ciphertext (string) with key
        '''
        mciphertext = b64decode(ciphertext)
        
        bs = Blowfish.block_size
        iv = mciphertext[:bs]
        mciphertext = mciphertext[bs:]

        cipher = Blowfish.new(self._key.encode("utf-8"), Blowfish.MODE_CBC, iv)
        msg = cipher.decrypt(mciphertext)

        last_byte = msg[-1]
        msg = msg[:- (last_byte if type(last_byte) is int else ord(last_byte))]
        return (msg.decode()) #"utf-8" by default


if __name__ == "__main__" :
    pwd = 'monmot depasse'
    
    test = Pwd_mgt()
    pwd_encrypt = test.encrypt(pwd)
    print(pwd_encrypt)
    print(test.decrypt(pwd_encrypt))
    print(test.decrypt("1BWtQ1e5oMUJ2oIC5sTs5VWMoIASpDhY"))
