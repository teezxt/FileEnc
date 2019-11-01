import wx
import socket
import os
import hashlib
import threading
import time 

from rsa_enc import rsa_keygen,rsa_encrypt,rsa_decrypt
from dec_file import dec_f
from job import Job

APP_START = 1

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

def rsade(e,n,msg):
    plain = decrypt(msg,e,n)
    return plain 
 
class Example(wx.Frame):
    def __init__(self,*args,**kw):
        self.app = wx.App()
        super(Example,self).__init__(*args,**kw)
        self.frame = wx.Frame(None,title = "Receiver",pos = (500,200),size = (500,400))
        self.task = Job()
        self.flag = True
        #self.frame = wx.Frame(None)
        self.InitUI()
        #self.server = socket.socket()

    def InitUI(self):
        self.pri_key,self.pub_key=get_keys()
        self.host_text = wx.TextCtrl(self.frame,pos = (5,5),value="127.0.0.1",size = (310,24))
        self.port_text = wx.TextCtrl(self.frame,pos = (318,5),value="7070",size = (60,24))
        self.open_button = wx.Button(self.frame,label = "连接",pos = (380,7),size = (50,20))
        self.open_button.Bind(wx.EVT_BUTTON,self.OnRequest) 
        self.stop_button = wx.Button(self.frame,label = "断开",pos = (435,7),size = (50,20))
        self.stop_button.Bind(wx.EVT_BUTTON,self.OnStop) 
        self.stop_button.Enable(False)
        self.content_text= wx.TextCtrl(self.frame,pos = (5,39),size = (475,300),style = wx.TE_MULTILINE)
        self.frame.Show() 
        self.app.MainLoop()
    
    def OnStop(self,e):
        #self.client.close()
        #self._flag = False
        try:
            self.task.pause()
        except:
            print("没有真的pause")
            pass
        self.stop_button.Enable(False)
        self.open_button.Enable(True)

    def recv_file(self,pub_keyser,sym_key):
        while True:
            print("接收文件")
            if self._flag is False:
                break
            file_con = b''
            while True:
                file_tmp = self.client.recv(1024)
                file_con += file_tmp
                if len(file_tmp)<1024:
                    break
            print("收到的文件长度",len(file_con))
            files = file_con.split(b',')
            file_con = files[0]
            filename_recv = files[1].decode('utf-8')
            print('文件名称',filename_recv)
            flag,cons = dec_f(file_con,pub_keyser,sym_key)
            #print(len(file_con))
            print('对比结果',flag)
            if flag:
                with open(filename_recv,"wb") as f:
                    f.write(cons)
                self.print_str += "安全收到文件"+ filename_recv +'\n'
            else:
                self.print_str += "文件"+filename_recv+'的完整性或机密性遭到破坏\n'
            self.content_text.SetValue(self.print_str)
    
    def OnRequest(self,e):
        self.open_button.Enable(False)
        self.stop_button.Enable(True)
        self.client = socket.socket()#声明socket类型，同时生成socke连接t对象
        host = self.host_text.GetValue()
        port = int(self.port_text.GetValue())
        self.print_str = self.content_text.GetValue()
        re = self.client.connect_ex((host,port))
        if re==0:
            self.print_str += "连接"+host+":"+str(port)+"成功\n"
            self.client.send(self.pub_key)
            pub_keyser = self.client.recv(1024)
            sym_key = self.client.recv(1024)
            #是对称密钥            
            #sym_key = self.client.recv(1024)
            sym_key = rsa_decrypt(self.pri_key,sym_key)
            print("收到的client私钥解密后的一次性密钥",sym_key)
            self.task.get_app(self.client,self.content_text,self.pri_key,pub_keyser,sym_key,self.open_button,self.stop_button)
            if self.flag:
                self.flag = False
                self.task.start()
            else:
                #self.task.get_app(self.client,self.content_text,self.pri_key,pub_keyser,sym_key,self.open_button,self.stop_button)
                self.task.resume()
            #self.recv_file(pub_keyser,sym_key)
            #t1 = threading.Thread(target=self.recv_file, args=(13,))
            #t1.start()  
            """filename_recv = client.recv(128).decode('utf-8')
            print('收到的文件的名称',filename_recv)
            filelen_recv = client.recv(64).decode('utf-8')"""    
        else:
            print('错误',re)
            self.print_str += "连接"+host+":"+str(port)+"失败\n"
        self.content_text.SetValue(self.print_str)


def main():
    #ex = wx.App()
    Example(None)
    #ex.MainLoop()
if __name__ == '__main__':
    main()