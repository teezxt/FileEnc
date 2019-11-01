#还有打开文件的部分需要做和wx需要做
#文件的存储和传输
#在接收端接到后就应该解密，将解密后的文件存储起来
#https://www.cnblogs.com/morries123/p/8568666.html
import wx
import socket
import os
import hashlib
import threading
import time 
import random
import string
from Crypto.PublicKey import RSA
from rsa_enc import rsa_keygen,rsa_encrypt,rsa_decrypt,rsa_sign,rsa_verify

from enc_file import enc_f
from job import Job
APP_START = 1
APP_STOP = 2
WORK = 0
 
random.seed(2019)

def rsade(e,n,msg):
    plain = rsa_decrypt(msg,e,n)
    return plain 

def rsaen(e,n,msg):
    cipher=rsa_encrypt(msg,e,n)
    return cipher

def get_keys():
    if os.path.isfile("master-private.pem") is False:
        flag = rsa_keygen()
    if True:
        with open("master-private.pem","rb") as f:
            pri_key = f.read()
            #pri_key = RSA.importKey(pri_key)
        with open("master-public.pem","rb") as f:
            pub_key = f.read()
            #pub_key = RSA.importKey(pub_key)
    else:
        exit()
    return pri_key,pub_key

class Example(wx.Frame):
    def __init__(self,*args,**kw):
        super(Example,self).__init__(*args,**kw)
        self.frame = wx.Frame(None,title = "Sender",pos = (500,200),size = (500,400))
        self.InitUI()
        self.num = 0
        self.pri_key,self.pub_key=get_keys()
        self.task = Job()
        self.task_flag = True
        #self.t1 = threading.Thread(target=self.OnListen, args=(13,))
        #self.server = socket.socket()

    def InitUI(self):
        self.start_button = wx.Button(self.frame,label = "开启",pos = (10,5),size = (50,24)) 
        self.start_button.Bind(wx.EVT_BUTTON,self.OnStart)    
        self.stop_button = wx.Button(self.frame,label = "停止",pos = (80,5),size = (50,24))
        self.stop_button.Bind(wx.EVT_BUTTON,self.OnStop)    # 绑定打开文件事件到open_button按钮上
        self.stop_button.Enable(False)
        self.start_button.Enable(True)
        self.file_text = wx.TextCtrl(self.frame,pos = (5,40),value="mingwen.txt",size = (350,24))
        self.open_button = wx.Button(self.frame,label = "传输文件",pos = (370,40),size = (100,24))
        self.open_button.Bind(wx.EVT_BUTTON,self.OnSend) 
        self.open_button.Enable(False)
        self.content_text= wx.TextCtrl(self.frame,pos = (5,75),size = (475,270),style = wx.TE_MULTILINE)
        #self.t1 = threading.Thread(target=self.OnListen, args=(13,))
        self.frame.Show() 

    def send_files(self):
        filename = self.file_text.GetValue()
        filename = filename.encode('utf-8')
        cipher_con = enc_f(filename,self.pri_key,one_key)
        cipher_con +=b','
        cipher_con += filename
        #conn.send(str(len(cipher_con)).encode('utf-8'))
        self.conn.send(cipher_con)
        self.print_str = self.content_text.GetValue()
        self.print_str += "已传输文件"+filename+"给"+self.addr[0]+":"+str(self.addr[1])+"\n"
        self.content_text.SetValue(self.print_str)
        #print("文件的长度是：",len(ciper_con))

    def OnSend(self,e):
        self.task.trans_file()

    def OnStart(self, e):
        self.stop_button.Enable(True)
        self.start_button.Enable(False)
        self.print_str = self.content_text.GetValue()
        self.print_str += "7070端口开启监听\n"
        self.content_text.SetValue(self.print_str)
        if self.task_flag:
            self.task_flag = False
            self.task.start()
            self.task.get_app(self.content_text,self.file_text,self.pri_key,self.pub_key,self.open_button)
        else:
            self.task.resume()

    def OnStop(self,e):
        self.start_button.Enable(True)
        self.stop_button.Enable(False)
        self.task.pause()
        self.print_str = self.content_text.GetValue()
        self.print_str += "7070端口关闭监听\n"
        self.content_text.SetValue(self.print_str)

def main():
    a,b=get_keys()
    """print(a)
    print('公钥')
    print(b)"""
    #公钥加密
    #content = rsa_encrypt(a,b'abckjsaug')
    #plain = rsa_decrypt(a,content)
    """mes = rsa_sign(a,b'abc')
    dec = rsa_verify(b,b'abc',mes)
    print(dec)
    cons=enc_f(a)
    print(cons)"""
    #print(plain)
    ex = wx.App()
    Example(None)
    ex.MainLoop()

if __name__ == '__main__':
    main()