from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
from hashlib import md5
from rsa_enc import rsa_keygen,rsa_encrypt,rsa_decrypt,rsa_sign,rsa_verify

def rsaen(e,n,msg):
    cipher=rsa_encrypt(msg,e,n)
    return cipher

def rsade(e,n,msg):
    plain = rsa_decrypt(msg,e,n)
    return plain 

def md5_file(content):
    m = md5()
    m.update(content)
    return m.hexdigest()

# 加密函数
def file_encrypt(text,key):
    key = key.encode('utf-8')
    mode = AES.MODE_CBC
    iv = b'qqqqqqqqqqqqqqqq'
    #text = add_to_16(text)
    cryptos = AES.new(key, mode, iv)
    cipher_text = cryptos.encrypt(text)
    # 因为AES加密后的字符串不一定是ascii字符集的，输出保存可能存在问题，所以这里转为16进制字符串
    return b2a_hex(cipher_text)


# 解密后，去掉补足的空格用strip() 去掉
def file_decrypt(text,key):
    iv = b'qqqqqqqqqqqqqqqq'
    mode = AES.MODE_CBC
    cryptos = AES.new(key, mode, iv)
    plain_text = cryptos.decrypt(a2b_hex(text))
    return plain_text

def dec_f(content,pri_key,one_key):
    d = file_decrypt(content,one_key)  
    conlen = len(d) - 128
    cons = d[:conlen]  
    abstr = d[-128:]
    dec = rsa_verify(pri_key,cons,abstr)
    #return cons
    return dec,cons
    #print("前摘要",abstr3)
    #print("后摘要",abstr2)

if __name__ == '__main__':
    
    dec_f()