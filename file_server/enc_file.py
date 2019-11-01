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
    key = key.encode('utf-8')
    iv = b'qqqqqqqqqqqqqqqq'
    mode = AES.MODE_CBC
    cryptos = AES.new(key, mode, iv)
    plain_text = cryptos.decrypt(a2b_hex(text))
    return plain_text

def enc_f(name,pri_key,one_key):
    #name = 'mingwen.txt'
    #name = input("输入需要传输的文件名：")
    with open(name,'rb') as f:
        content = f.read()
    f.close()
    lens = len(content)
    num = lens%16
    if num!=0:
    	pass
        #print(num)
    #print(type(content))
    for i in range(16-num):
        content+=b' '
    abstr = rsa_sign(pri_key,content)
    print("对文本进行取摘要后用server的私钥签名：",abstr)
    #abstr = md5_file(content)
    #abstr = rsa_encrypt(pri_key,abstr.encode(''utf-8))
    content += abstr
    e = file_encrypt(content,one_key)
    print("用AES算法加密后的传输文件长度",len(e))
    return e  
    """d = file_decrypt(e,'securitysecurity')  
    conlen = len(d) - 128
    cons = d[:conlen]  
    abst = d[-128:]
    return cons,abst"""
    """abstr2 = md5_file(cons) #chong jisuan
    abstr3 = rsade(157,959,abst) #这是
    print("前摘要",abstr3)
    print("后摘要",abstr2)"""

if __name__ == '__main__':
	
	enc_f()