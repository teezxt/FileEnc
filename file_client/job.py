#!/usr/bin/env python
# coding: utf-8
import threading
import time
import socket
import string
import random
from Crypto.PublicKey import RSA
from rsa_enc import rsa_keygen,rsa_encrypt,rsa_decrypt,rsa_sign,rsa_verify
from dec_file import dec_f

class Job(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(Job, self).__init__(*args, **kwargs)
        self.__flag = threading.Event()     # 用于暂停线程的标识
        self.__flag.set()       # 设置为True
        self.__running = threading.Event()      # 用于停止线程的标识
        self.__running.set()      # 将running设置为True  

    def run(self):
        while self.__running.isSet():
            self.__flag.wait()      # 为True时立即返回, 为False时阻塞直到内部的标识位为True后返回
            #self.recv_file()
            #file_con = b''
            try:
                #print("真的继续了")
                file_len = self.client.recv(64)
                file_len = int(file_len.decode('utf-8'))
                file_con = self.client.recv(file_len+16)
                print("收到的文件长度",len(file_con))
                files = file_con.split(b',')
                file_con = files[0]
                filename_recv = files[1].decode('utf-8')
                print('文件名称',filename_recv)
                flag,cons = dec_f(file_con,self.pub_key,self.one_key)
                #print(len(file_con))
                print('对比结果',flag)
                print_str = self.content_text.GetValue()
                if flag:
                    with open(filename_recv,"wb") as f:
                        f.write(cons)
                    print_str += "安全收到文件"+ filename_recv +'\n'
                else:
                    print_str += "文件"+filename_recv+'的完整性或机密性遭到破坏\n'
                self.content_text.SetValue(print_str)
            except:
                pass
    
    def pause(self):
        self.client.close()
        self.__flag.clear()     # 设置为False, 让线程阻塞

    def resume(self):
        self.__flag.set()    # 设置为True, 让线程停止阻塞
        
    def stop(self):
        self.__flag.set()
        self.client.close
        self.__running.clear()        # 设置为False

    def get_app(self,client,content_text,pri_key,pub_key,one_key,open_button,stop_button):
        self.client = client
        self.content_text = content_text
        self.open_button = open_button
        self.stop_button = stop_button
        self.pub_key = pub_key
        self.pri_key = pri_key
        self.one_key = one_key


    

