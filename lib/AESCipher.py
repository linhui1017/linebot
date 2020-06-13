# AES 
from hashlib import md5
import base64
import json
from Crypto import Random
from Crypto.Cipher import AES


class AESCipher:
    """
    AES/ECB/PKCS#7 加密算法
    """
    BLOCK_SIZE = 16

    def __init__(self, key, md5Encode = True):
        self.key = md5(key.encode('utf8')).hexdigest() if md5Encode else key

    def pkcs7_pad(self, s):
        length = self.BLOCK_SIZE - (len(s) % self.BLOCK_SIZE)
        s += bytes([length]) * length
        return s

    def pkcs7_unpad(self, s):
        """
        unpadding according to PKCS #7
        @param s: string to unpad
        @type s: byte
        @rtype: byte
        """
        sd = -(s[-1])
        return s[0:sd]

    def encrypt(self, plain_text):
        if (plain_text is None) or (len(plain_text) == 0):
            raise ValueError('input text cannot be null or empty set')

        plain_bytes = plain_text.encode('utf-8')
        raw = self.pkcs7_pad(plain_bytes)

        #iv = Random.new().read(AES.block_size)
        #cipher = AES.new(self.key, AES.MODE_ECB, iv)
        #cipher_text = self.base64_encode(iv + cipher_bytes)

        iv = self.key.encode('utf8')
        cipher = AES.new(self.key, AES.MODE_ECB)
        cipher_bytes = cipher.encrypt(raw)

        cipher_text = self.base64_encode(cipher_bytes)
        return cipher_text

    def decrypt(self, cipher_text):

        cipher_bytes = self.base64_decode(cipher_text)
        #iv = cipher_bytes[:AES.block_size]
        #cipher_data = cipher_bytes[AES.block_size:]
        #cipher = AES.new(self.key, AES.MODE_ECB, iv)

        iv = self.key.encode('utf8')
        cipher_data = cipher_bytes
        cipher = AES.new(self.key, AES.MODE_ECB)
        plain_pad = cipher.decrypt(cipher_data)
        plain_text = self.pkcs7_unpad(plain_pad)
        return plain_text.decode('utf8')

    def base64_encode(self, bytes_data):
        """
        Base64Url
        加base64
        :type bytes_data: byte
        :rtype return: string
        """
        output = base64.b64encode(bytes_data).decode('utf8')
        output = output.split('=')[0]
        output = output.replace('+', '-')
        output = output.replace('/', '_')
        #return (base64.urlsafe_b64encode(bytes_data)).decode('utf8')
        return output


    def base64_decode(self, str_data):
        """
        Base64Url
        解base64
        :type str_data: string
        :rtype return: byte
        """
        output = str_data
        output = output.replace('-', '+')
        output = output.replace('_', '/')

        pad = len(output) % 4

        if(pad == 0):
            pass
        elif(pad == 2):
            output += "=="
        elif(pad == 3):
            output += "="
        else:
            raise Exception("Illegal base64url string!")   

        return base64.b64decode(output.encode('utf-8'))        

        #return base64.urlsafe_b64decode(str_data) 

