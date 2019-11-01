#!/usr/bin/env python
# coding: utf-8
import threading
import time
import socket
import string
import random
from Crypto.PublicKey import RSA
from rsa_enc import rsa_keygen,rsa_encrypt,rsa_decrypt,rsa_sign,rsa_verify
from enc_file import enc_f

class Job(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(Job, self).__init__(*args, **kwargs)
        self.__flag = threading.Event()     # 用于暂停线程的标识
        self.__flag.set()       # 设置为True
        self.__running = threading.Event()      # 用于停止线程的标识
        self.ip = '127.0.0.1'  #可设置
        self.port = 7070
        self.__running.set()      # 将running设置为True
        self.allconn = []    

    #本机内网的IP
    def get_ip(self):
        myname = socket.getfqdn(socket.gethostname())
        self.ip = socket.gethostbyname(myname)

    def run(self):
        while self.__running.isSet():
            self.__flag.wait()      # 为True时立即返回, 为False时阻塞直到内部的标识位为True后返回
            self.server = socket.socket()
            self.server.bind((self.ip, self.port))
            #self.allcon = [] #这个是用于多连接的
            self.server.listen(5)  
            while True:
                if self .__flag.isSet() is False:
                    break
                #print('kai qi jian ting')
                try:
                    conn,addr = self.server.accept()
                    self.send_key(conn,addr)
                    self.allconn = []
                    self.alladdr = []
                    self.alladdr.append(addr)
                    self.allconn.append(conn)
                except:
                    pass
        #print('xun huan wanquan jieshu')

    def pause(self):
        for c in self.allconn:
            #print("close one connection")
            c.close()
        self.server.close()
        self.open_button.Enable(False)
        #print("guan bi jian ting")
        self.__flag.clear()     # 设置为False, 让线程阻塞

    def resume(self):
        self.__flag.set()    # 设置为True, 让线程停止阻塞

    def stop(self):
        self.__running.clear()        # 设置为False

    def get_app(self,content_text,file_text,pri_key,pub_key,open_button):
        self.content_text = content_text
        self.file_text = file_text
        self.open_button = open_button
        self.pub_key = pub_key
        self.pri_key = pri_key

    def send_key(self,con,addr):
        #print("看看addr的类型",addr)
        self.pub_keycli = con.recv(1024) #收到的公钥
        #con.send(self.pub_key)
        keys = string.ascii_letters
        print_str = self.content_text.GetValue()
        print_str += "与"+addr[0]+":"+str(addr[1])+"建立连接\n"
        self.content_text.SetValue(print_str)
        self.open_button.Enable(True)
        #pri_key = pri_key.decode('utf-8')
        self.one_key = ""
        for i in range(16):
            self.one_key += random.choice(keys)
        self.one_keys = self.one_key.encode('utf-8')
        print("一次性密钥",self.one_keys)
        sym_key = rsa_encrypt(self.pub_keycli,self.one_keys)
        print("Client公钥加密后的一次性密钥",sym_key)
        con.send(self.pub_key)
        con.send(sym_key)

    def trans_file(self):
        con = self.allconn[0]
        addr = self.alladdr[0]
        filename = self.file_text.GetValue()
        filename2 = filename
        filename = filename.encode('utf-8')
        cipher_con = enc_f(filename,self.pri_key,self.one_key)
        cipher_con +=b','
        cipher_con += filename
        #conn.send(str(len(cipher_con)).encode('utf-8'))
        con.send(str(len(cipher_con)).encode('utf-8'))
        con.send(cipher_con)
        print_str = self.content_text.GetValue()
        print_str += "已传输文件"+filename2+"给"+addr[0]+":"+str(addr[1])+"\n"
        self.content_text.SetValue(print_str)

