from Crypto import Random
from Crypto.Hash import SHA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.Signature import PKCS1_v1_5 as Signature_pkcs1_v1_5
from Crypto.PublicKey import RSA
import base64
from Crypto.Hash import SHA

def rsa_keygen():
	random_generator = Random.new().read
	rsa = RSA.generate(1024, random_generator)
	private_pem = rsa.exportKey()
	with open("master-private.pem", "wb") as f:
		f.write(private_pem)
	public_pem = rsa.publickey().exportKey()
	with open("master-public.pem", "wb") as f:
		f.write(public_pem)

def rsa_encrypt(rsakey,message):
	rsakey = RSA.importKey(rsakey)
	cipher = Cipher_pkcs1_v1_5.new(rsakey)
	cipher_text = cipher.encrypt(message)
	return cipher_text
	#cipher_text = base64.b64encode(cipher.encrypt(message))

def rsa_decrypt(rsakey,message):
	rsakey = RSA.importKey(rsakey)
	cipher = Cipher_pkcs1_v1_5.new(rsakey)
	sentinel = None
	cipher_text = cipher.decrypt(message,sentinel)
	return cipher_text
	#cipher_text = base64.b64encode(cipher.encrypt(message))

def rsa_sign(rsakey,message):
	rsakey = RSA.importKey(rsakey)
	cipher = Signature_pkcs1_v1_5.new(rsakey)
	hs = SHA.new(message)
	cipher_text = cipher.sign(hs)
	return cipher_text

#key,abstract,signatrue
def rsa_verify(rsakey,message,signature):
	rsakey = RSA.importKey(rsakey)
	cipher = Signature_pkcs1_v1_5.new(rsakey)
	hs = SHA.new(message)
	return cipher.verify(hs,signature)

