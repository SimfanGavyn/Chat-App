from socket import *
import json
import tkinter as tk
from tkinter import filedialog
import struct
# from tkinter import ttk
import threading
from certificate import Certificate
from rsa import RSA, getPrimeNum
from md5 import md5
from time import ctime
from caesar import Caesar
from playfair import Playfair
from pydes import des
from dh import DH
import os
import base64
import cv2
from vclient import Video_Client
from vserver import Video_Server
import random
import time

# define color
colors = {
    'lightGray': '#3E4149',
    'darkGray': '#292421',
    'white': '#DCDCDC',
    'black': '#000000',
    'green': '#00FF00',
    'blue': '#0000FF'
}

class Client():
    def __init__(self):
        self.isConnect = False
        self.selfInfo = {}

    def connect(self):
        """连接服务器"""
        if not self.isConnect:
            self.tcpCliSock = socket(AF_INET, SOCK_STREAM)
            self.tcpCliSock.connect(ADDR)
            self.isConnect = True
            print ("__Connect to server.")
        else:
            print ("__Already connect.")

    def disConnect(self):
        """断开服务器"""
        self.tcpCliSock.close()

    def notification(self, message):
        notice = tk.Tk()
        notice.geometry('+575+410')
        notice.title("Notification!")
        notice.configure(background=colors['black'])
        notice.attributes('-topmost',1)

        tk.Label(notice,font = ('Arial, 15'),
                bg = colors['black'],text = message,
                fg = colors['green']).pack(padx = 10,
                pady = 10)
        # tk.Button(notice, text = "OK",
        #         # command = lambda: self.showOut(notice, originalWindow),
        #         command = notice.destroy(),
        #         highlightbackground = colors['black']).pack(padx = 5,
        #         pady = 5)
        # notice.protocol('WM_DELETE_WINDOW',
        #         # lambda: self.showOut(notice, originalWindow)
        #         notice.destroy()
        #         )
        # print("I am not out")
        notice.mainloop()
        # print("I am out now")

    # def showErr(self, info):
    #     """错误提示界面"""
    #     errTk = tk.Tk()
    #     errTk.geometry('200x120')
    #     errTk.title("Error!")
    #     tk.Label(errTk,font = ('Arial, 15'),
    #             bg = colors['black'],text = info,
    #             fg = colors['green']).pack(padx = 5,
    #             pady = 20, fill = 'x')
    #     bt = tk.Button(errTk, text = "确定",
    #         command = errTk.destroy,
    #         highlightbackground = colors['black']).pack()
    #     errTk.mainloop()

    class Login():
        """登录界面"""
        def __init__(self, father):
            self.father = father
            self.LOGIN = "login"
            self.SIGNUP = "signup"

        def signUpOrLogin(self, entryName, entryPassword, loginWindow, mod):
            username = entryName.get()
            # TODO MD5
            password = md5(entryPassword.get())
            self.father.username = username
            data = {
                "type": mod,
                "username": username,
                "password": password
            }
            jData = json.dumps(data)
            try:
                self.father.connect()
            except Exception as e:
                print (e)
                # self.father.notification("Connect Error: Can't connect server.", loginWindow)
                print("CONNECT ERROR: Can't connect server.")
                return False
            else:
                socket = self.father.tcpCliSock
                socket.send(jData.encode())
                recvJData = socket.recv(BUFSIZ).decode()
                recvJData = json.loads(recvJData)
                if recvJData["username"] == username and \
                        recvJData["password"] == password and \
                        recvJData["status"] == True and \
                        (recvJData["type"] == self.SIGNUP or \
                        recvJData["type"] == self.LOGIN):
                    

                    loginWindow.destroy()
                    if recvJData["type"] == self.SIGNUP:
                        self.father.notification("Sign Up Successfully!")
                    else:
                        self.father.notification("Login Successfully!")
                    mainFrame = self.father.MainFrame(self.father)
                    mainFrame.__main__()
                else:
                    if recvJData["info"]:
                        print(recvJData["info"])
                    else:
                        print("UNKNOWN ERROR.")


        def window(self):
            """login GUI"""
            login = tk.Tk()
            login.geometry('+525+325')
            login.attributes('-topmost',1)
            login.title('FBI Warning')
            login.configure(background=colors['black'])
            
            # photo
            photo=tk.PhotoImage(file="resource/name.gif")
            logo=tk.Label(image=photo,bg=colors['lightGray'])
            logo.image=photo
            logo.grid(row=0,column=0,rowspan=2,columnspan=2,sticky=tk.W+tk.E+tk.N+tk.S, padx=5, pady=5)

            # username
            tk.Label(login, font = ("Arial, 15"),
                    bg = colors['black'], text = "User Name:",
                    fg = colors['green']).grid(row = 2,
                    sticky = tk.W, padx = 5, pady = 5)
            entryName = tk.Entry(login, bg = colors['black'],
                    fg = colors['green'],
                    insertbackground = colors['white'],
                    highlightbackground = colors['lightGray'],
                    selectbackground = colors['blue'],
                    selectforeground = colors['green'])
            entryName.grid(row = 2, column = 1, padx = 5, pady = 5)
            entryName.focus_set()
            
            # password
            tk.Label(login, font = ("Arial, 15"),
                    bg = colors['black'],text = "Password:",
                    fg = colors['green']).grid(row = 3,
                    sticky = tk.W, padx = 5, pady = 5)
            entryPassword = tk.Entry(login, bg=colors['black'],
                    fg = colors['green'], show="*",
                    insertbackground = colors['white'],
                    highlightbackground=colors['lightGray'],
                    selectbackground = colors['blue'],
                    selectforeground = colors['green'])
            entryPassword.grid(row = 3, column=1, padx=5, pady=5)
            entryPassword.bind('<Key-Return>',
                    lambda x : self.signUpOrLogin(entryName,
                    entryPassword, login, self.LOGIN))
            
            # signup or login
            signUpButton = tk.Button(login, text = "Sign up",
                    highlightbackground = colors['black'],
                    command = lambda : self.signUpOrLogin(entryName,
                    entryPassword, login, self.SIGNUP)
                    )
            signUpButton.grid(row=4,column=0, sticky = tk.W,padx=5, pady=5)
            loginButton = tk.Button(login, text = "Login",
                    highlightbackground = colors['black'],
                    command = lambda : self.signUpOrLogin(entryName,
                    entryPassword, login, self.LOGIN))
            loginButton.grid(row=4,column=1, sticky = tk.E,padx=5, pady=5)
            
            # start this GUI
            login.focus_force()
            login.mainloop()

        def __main__(self):
            self.window()

    class MainFrame():
        """聊天主窗口"""
        def __init__(self, father):
            self.father = father
            self.socket = father.tcpCliSock # may raise a Exception
            self.rSocket = None
            self.sSocket = None

        class ListenThread(threading.Thread):
            """Socket监听线程，对收到的信息作出相应反馈"""
            def __init__(self, socket, father):
                threading.Thread.__init__(self)
                self.father = father
                self.socket = socket

            def run(self):
                while True:
                    try:
                        jData = self.socket.recv(BUFSIZ).decode()
                        data = json.loads(jData)
                    except:
                        break
                    print ("__receive__" + jData)
                    switch = {
                            "list": self.list,
                            "singleChat": self.chat,
                            "groupChat": self.chat,
                            "returnCertificate": self.send,
                            "communicate": self.communicate,
                            "file": self.sFile,
                            "video": self.sVideo
                            }
                    switch[data['type']](data)
                print ("结束监听")

            def sVideo(self, data):
                port = data['port']
                ip = data['ip']


                vClient = Video_Client(ip, port, 1, 4)
                time.sleep(0.5)
                vClient.run()


            def sFile(self, data):
                signature = data['signature']
                
                fileAddr = data['fileAddr']
                currentPath = '/Users/simon/Desktop/personal'
                (filepath, filename) = os.path.split(fileAddr)
                fileData = data['fileData']
                # r = RSA(0)
                logArea = self.father.logArea
                textArea = self.father.textArea
                if md5(fileData) == signature:
                    log = ctime() + " Verify Success"
                    text = "[ You receive a file from " + data['from'] + ' ' + ctime() + "]\n"

                else:
                    log = ctime() + " Verify Fail"
                    text = ""
                logArea.insert(tk.END, log + '\n\n')
                logArea.see(tk.END)
                textArea.insert(tk.END, text)
                textArea.see(tk.END)
                filePath = currentPath + '/fileResource/' + data['to']
                    #  + '/' + filename
                ifExist = os.path.exists(filePath)
                if not ifExist:
                    os.makedirs(filePath)
                # print(filePath)
                filePath += '/' + filename
                with open(filePath, 'wb') as f:
                    code = base64.b64decode(fileData.encode())
                    f.write(code)
                

            def communicate(self, data):
                if data.__contains__('mB'):
                    mB = data['mB']
                    
                    key = pow(mB, self.father.father.selfInfo['secretA'], 
                            self.father.father.selfInfo['pAndg'][0])
                    self.father.father.selfInfo['key'] = key
                    data['mA'] = self.father.father.selfInfo['mA']
                    data['type'] = 'singleChat'
                    
                    temp = data['to']
                    data['to'] = data['from']
                    data['from'] = temp

                    jData = json.dumps(data)
                    self.socket.send(jData.encode())
                    print ('__send__' + jData)
                    
                else:
                    receiverCertificate = data['certificate']
                    pAndg= receiverCertificate['pAndg']
                    self.father.father.selfInfo['pAndg'] = pAndg
                    self.father.father.selfInfo['secretB'] = getPrimeNum(20)
                    mB = pow(pAndg[1], self.father.father.selfInfo['secretB'], pAndg[0])
                    self.father.father.selfInfo['mB'] = mB
                    data['mB'] = mB

                    jData = json.dumps(data)
                    self.socket.send(jData.encode())
                    print ('__send__' + jData)
                


            def list(self, data):
                """刷新列表"""
                listbox = self.father.listbox
                list = data['list']
                listbox.delete(0, tk.END) # clear
                for l in list:
                    listbox.insert(tk.END, l) # insert
                logArea = self.father.logArea
                log = ctime() + " Refresh Online List"
                logArea.insert(tk.END, log + '\n\n')
                logArea.see(tk.END)

            def chat(self, data):
                """接收聊天信息并打印"""
                sender = data['from']
                receiver = data['to']
                logArea = self.father.logArea
                log = ctime() + " Receive Message\n\n"

                encryptedMessage = data['encryptedMessage']
                encryptedKey = data['encryptedKey']
                signature = data['signature']
                senderPubKey = data['senderPubKey']
                decryptionType = self.father.father.selfInfo['decryptionType']
                # message = ''
                r = RSA(0)
                priKey = self.father.father.selfInfo['priKey']
                key = r.decryption(encryptedKey, priKey)
                if self.father.father.selfInfo['communicationType'] == 'rsa':
                    
                    # priKey = self.father.father.selfInfo['priKey']                    
                    if len(encryptedMessage) > 5:
                        result = r.verify(encryptedMessage[0:6], signature, senderPubKey)
                    else:
                        result = r.verify(encryptedMessage, signature, senderPubKey)
                    if result:
                        log += ctime() + " Verify Successfully\n\n"
                        # father.father.logArea.insert(tk.END)
                        key = r.decryption(encryptedKey, priKey)
                        if decryptionType == 'caesar':
                            c = Caesar()
                            key = int(key)
                            message = c.decryption(encryptedMessage, key)
                            # pass
                        elif decryptionType == 'playfair':
                            p = Playfair(0)
                            p.generateMatrix(key)
                            message = p.decryption(encryptedMessage)
                            # pass
                        elif decryptionType == 'des':
                            d = des()
                            message = d.decrypt(key, encryptedMessage)
                        else:
                            d = des()
                            less = data['less']
                            # print("--------------------",key1, key2, encryptedMessage)
                            message = d.tdecrypt(key[2:10], key[14:22], encryptedMessage)
                            
                            message = message[0:-less]
                            # print("--------------------",message)
                            # pass
                    else:
                        # 输出不合格
                        pass
                else:
                    r = RSA(0)
                    if len(encryptedMessage) > 5:
                        result = r.verify(encryptedMessage[0:6], signature, senderPubKey)
                    else:
                        result = r.verify(encryptedMessage, signature, senderPubKey)
                    if result:
                        log += ctime() + " Verify Successfully\n\n"
                        if decryptionType == 'caesar':
                            key = self.father.father.selfInfo['key']
                            c = Caesar(key)
                            ct, secretKey = c.encryption('aaa')
                            message = c.decryption(encryptedMessage[0], secretKey)
                            print('-----------pass')
                        elif decryptionType == 'playfair':
                            p = Playfair(0)
                            p.generateMatrix(key)
                            message = p.decryption(encryptedMessage)
                        elif decryptionType == 'des':
                            d = des()
                            message = d.decrypt(key, encryptedMessage)
                        else:
                            d = des()
                            less = data['less']
                            
                            message = d.tdecrypt(key[2:10], key[14:22], encryptedMessage)
                            
                            message = message[0:-less]
                            # pass
                    else:
                        print('-----------not pass')
                        pass
                # print("i am here")
                textArea = self.father.textArea
                text = '['+ sender + ' -> ' + receiver + ' ' + \
                        ctime() + ']\n\t' + message + '\n'
                textArea.insert(tk.END, text)
                textArea.see(tk.END)
                
                logArea.insert(tk.END, log)
                logArea.see(tk.END)    

                print("i am here")
                
            def send(self, data):
                receiverCertificate = data['certificate']

                inputEntry = self.father.inputEntry
                message = inputEntry.get()
                
                sender = self.father.father.username
                receiver = receiverCertificate['username']
                encryptionType = receiverCertificate['encryptionType']
                receiverPublicKey = receiverCertificate['publicKey']
                communicationType = receiverCertificate['communicationType']
                less = 0
                logArea = self.father.logArea
                log = ctime() + " Receive Certificate\n\n"

                if communicationType == 'rsa':
                    log += ctime() + " Communication Type: RSA\n\n"
                    # logArea.insert(tk.END, log + '\n\n')
                    # logArea.see(tk.END)
                    if encryptionType == 'caesar':
                        # encryption = Caesar()
                        c = Caesar()
                        cypherText, key = c.encryption(message)
                        r = RSA(0)
                        encryptedKey = r.encryption(key, receiverPublicKey)
                        
                        # print(cypherText, self.father.father.selfInfo['priKey'])
                        if len(cypherText) > 5:
                            signature = r.sign(cypherText[0:6], self.father.father.selfInfo['priKey'])
                        else:
                            signature = r.sign(cypherText, self.father.father.selfInfo['priKey'])
                        
                        data = {
                            'type': 'singleChat',
                            'encryptedMessage': cypherText,
                            'encryptedKey': encryptedKey,
                            'signature': signature,
                            'to': receiver,
                            'from': sender
                        }
                        log += ctime() + " Encryption Type: Caesar\n\n"
                        # logArea.insert(tk.END, log + '\n\n')
                        # logArea.see(tk.END)
                    elif encryptionType == 'playfair':
                        p = Playfair()
                        cypherText, key = p.encryption(message)
                        r = RSA(0)
                        encryptedKey = r.encryption(key, receiverPublicKey)

                        if len(cypherText) > 5:
                            signature = r.sign(cypherText[0:6], self.father.father.selfInfo['priKey'])
                        else:
                            signature = r.sign(cypherText, self.father.father.selfInfo['priKey'])

                        data = {
                            'type': 'singleChat',
                            'encryptedMessage': cypherText,
                            'encryptedKey': encryptedKey,
                            'signature': signature,
                            'to': receiver,
                            'from': sender
                        }    
                        log += ctime() + " Encryption Type: Playfair\n\n"
                    elif encryptionType == 'des':
                        d = des()
                        key, temp = d.randomkey()
                        
                        cypherText = d.encrypt(key, message)
                        # if message
                        r = RSA(0)
                        encryptedKey = r.encryption(key, receiverPublicKey)

                        if len(cypherText) > 5:
                            signature = r.sign(cypherText[0:6], self.father.father.selfInfo['priKey'])
                        else:
                            signature = r.sign(cypherText, self.father.father.selfInfo['priKey'])

                        data = {
                            'type': 'singleChat',
                            'encryptedMessage': cypherText,
                            'encryptedKey': encryptedKey,
                            'signature': signature,
                            'to': receiver,
                            'from': sender
                        }    
                        log += ctime() + " Encryption Type: DES\n\n"
                        # pass
                    else:
                        d = des()
                        keys = d.randomkey()
                        # less = 0
                        if len(message) % 8 != 0:
                            less = 8 - (len(message) - len(message) // 8 * 8)
                            for i in range(less):
                                message += '0'
                        print(message)
                        # print("--------------------", keys[0], keys[1])
                        cypherText = d.tencrypt(keys[0], keys[1], message)
                        print("--------------------", keys[0], keys[1], cypherText)
                        r = RSA(0)
                        encryptedKey = r.encryption(keys, receiverPublicKey)

                        if len(cypherText) > 5:
                            signature = r.sign(cypherText[0:6], self.father.father.selfInfo['priKey'])
                        else:
                            signature = r.sign(cypherText, self.father.father.selfInfo['priKey'])

                        data = {
                            'less': less,
                            'type': 'singleChat',
                            'encryptedMessage': cypherText,
                            'encryptedKey': encryptedKey,
                            'signature': signature,
                            'to': receiver,
                            'from': sender
                        }    
                        log += ctime() + " Encryption Type: 3DES\n\n"
                else:
                    mA = data['mA']
                    key = pow(mA, self.father.father.selfInfo['secretB'],
                            self.father.father.selfInfo['pAndg'][0])
                    if encryptionType == 'caesar':
                        c = Caesar(key)
                        cypherText = c.encryption(message)
                    
                        r = RSA(0)
                        encryptedKey = r.encryption(key, receiverPublicKey)

                        if len(cypherText) > 5:
                            signature = r.sign(cypherText[0:6], self.father.father.selfInfo['priKey'])
                        else:
                            signature = r.sign(cypherText, self.father.father.selfInfo['priKey'])

                        data = {
                            'type': 'singleChat',
                            'encryptedMessage': cypherText,
                            'encryptedKey': encryptedKey,
                            'signature': signature,
                            'to': receiver,
                            'from': sender
                        }    
                        log += ctime() + " Encryption Type: Playfair\n\n"
                    elif encryptionType == 'playfair':
                        p = Playfair()
                        cypherText, key = p.encryption(message)
                        r = RSA(0)
                        encryptedKey = r.encryption(key, receiverPublicKey)

                        if len(cypherText) > 5:
                            signature = r.sign(cypherText[0:6], self.father.father.selfInfo['priKey'])
                        else:
                            signature = r.sign(cypherText, self.father.father.selfInfo['priKey'])

                        data = {
                            'type': 'singleChat',
                            'encryptedMessage': cypherText,
                            'encryptedKey': encryptedKey,
                            'signature': signature,
                            'to': receiver,
                            'from': sender
                        }    
                        log += ctime() + " Encryption Type: Playfair\n\n"
                    elif encryptionType == 'des':
                        d = des()
                        key, temp = d.randomkey()
                        
                        cypherText = d.encrypt(key, message)
                        # if message
                        r = RSA(0)
                        encryptedKey = r.encryption(key, receiverPublicKey)

                        if len(cypherText) > 5:
                            signature = r.sign(cypherText[0:6], self.father.father.selfInfo['priKey'])
                        else:
                            signature = r.sign(cypherText, self.father.father.selfInfo['priKey'])

                        data = {
                            'type': 'singleChat',
                            'encryptedMessage': cypherText,
                            'encryptedKey': encryptedKey,
                            'signature': signature,
                            'to': receiver,
                            'from': sender
                        }    
                        log += ctime() + " Encryption Type: DES\n\n"
                        # pass
                    else:
                        d = des()
                        keys = d.randomkey()
                        # less = 0
                        if len(message) % 8 != 0:
                            less = 8 - (len(message) - len(message) // 8 * 8)
                            for i in range(less):
                                message += '0'
                        print(message)
                        # print("--------------------", keys[0], keys[1])
                        cypherText = d.tencrypt(keys[0], keys[1], message)
                        print("--------------------", keys[0], keys[1], cypherText)
                        r = RSA(0)
                        encryptedKey = r.encryption(keys, receiverPublicKey)

                        if len(cypherText) > 5:
                            signature = r.sign(cypherText[0:6], self.father.father.selfInfo['priKey'])
                        else:
                            signature = r.sign(cypherText, self.father.father.selfInfo['priKey'])

                        data = {
                            'less': less,
                            'type': 'singleChat',
                            'encryptedMessage': cypherText,
                            'encryptedKey': encryptedKey,
                            'signature': signature,
                            'to': receiver,
                            'from': sender
                        }    
                        log += ctime() + " Encryption Type: 3DES\n\n"
                    # pAndg = receiverCertificate['pAndg']
                    # self.father.father.selfInfo['secretB'] = getPrimeNum(20)
                    # mB = pow(pAndg[1], self.father.father.selfInfo['secretB'], pAndg[0])
                    # receiverCertificate['mB'] = mB
                    pass
                jData = json.dumps(data)
                self.socket.send(jData.encode())
                print ('__send__' + jData)

                # update log
                log += ctime() + " Send Message Success\n\n"
                logArea.insert(tk.END, log)
                logArea.see(tk.END)

                # update text
                textArea = self.father.textArea
                if less != 0:
                    message = message[0:-less]
                text = '['+ sender + ' -> ' + receiver + ' ' + \
                        ctime() + ']\n\t' + message + '\n'
                textArea.insert(tk.END, text)
                textArea.see(tk.END)
                
                inputEntry.delete(0, tk.END)

                
                
        class Window():
            def __init__(self, father):
                self.father = father

            def refresh(self, socket):
                """点击刷新按钮"""
                data = {"type": "list"}
                jData = json.dumps(data)
                socket.send(jData.encode())

            

            def requestCertificate(self, socket, nameLabel):
                """点击发送按钮"""
                # text = inputEntry.get()
                toName = nameLabel['text']
                if toName == 'Unseleted':
                    message = self.father.inputEntry.get()
                    text = '['+ self.father.father.username + ' -> ' + toName + ' ' + \
                        ctime() + ']\n\t' + message + '\n'
                    self.father.textArea.insert(tk.END, text)
                    self.father.textArea.see(tk.END)
                    self.father.inputEntry.delete(0, tk.END)
                    # pass
                else:
                    username = self.father.father.username
                    

                    # 私聊
                    data = {'type': 'requestCertificate',
                            # 'msg': text,
                            'to': toName, 'from': username}
                    

                    jData = json.dumps(data)
                    socket.send(jData.encode())
                    print ('__send__' + jData)
                    # inputEntry.delete(0, tk.END)

            def changeSendTo(self, listbox, nameLabel):
                """双击选择列表"""
                try:
                    nameLabel['text'] = listbox.get(listbox.curselection()) 
                except:
                    pass # nothing choose

            

            def uploadFile(self, socket, nameLabel):
                selectFile = tk.filedialog.askopenfilename()
                print(selectFile)
                toName = nameLabel['text']
                username = self.father.father.username
                data = {
                    'type': 'file',
                    'fileAddr': selectFile,
                    'to': toName,
                    'from': username
                }
                logArea = self.father.logArea
                textArea = self.father.textArea

                log = ctime() + " Send File Success"
                text = "[ You send a file to " + toName + ' ' + ctime() + "]\n"

                with open(selectFile, 'rb') as f:
                    fileData = base64.b64encode(f.read()).decode()
                data['fileData'] = fileData
                r = RSA(0)
                data['signature'] = md5(fileData)
                jData = json.dumps(data)
                socket.send(jData.encode())
                print ('__send__' + jData)
                logArea.insert(tk.END, log + '\n\n')
                logArea.see(tk.END)
                textArea.insert(tk.END, text)
                textArea.see(tk.END)

            def videoCall(self, socket, nameLabel):
                receiver = nameLabel['text']
                username = self.father.father.username
                port = random.randint(5000, 8000)
                ip = gethostbyname(gethostname())
                data = {
                    'type': 'video',
                    'to': receiver,
                    'from': username,
                    'port': port,
                    'ip': ip
                }

                jData = json.dumps(data)
                socket.send(jData.encode())
                print ('__send__' + jData)
                vServer = Video_Server(port, 4)
                vServer.run()

            def __main__(self):
                father = self.father
                chatroom = tk.Tk()
                chatroom.geometry('600x400+425+225')
                chatroom.title('91 Chatroom for ' + self.father.father.username)
                # chatroom.attributes('-topmost',1)

                # backgroud
                frame = tk.Frame(chatroom, bg=colors['black'],
                        width = 600, height = 400)
                frame.place(x = 0, y = 0)

                # container
                textArea = tk.Text(frame, bg = colors['black'],
                        fg = colors['green'],
                        highlightbackground = colors['lightGray'], 
                        selectbackground = colors['blue'],
                        selectforeground = colors['green'],
                        width = 60, height = 22, bd = 0)
                textArea.place(x = 10, y = 10, anchor = tk.NW)
                textArea.bind('<KeyPress>', lambda x : "break")
                father.textArea = textArea
                # textArea.focus_set()
                # choose
                tk.Label(frame, text = "Select Receiver:",
                        bg = colors['black'],
                        fg = colors['green']).place(
                        x = 460, y = 10, anchor = tk.NW)
                listbox = tk.Listbox(frame, width = 14, height = 7,
                        bg = colors['darkGray'],
                        fg = colors['green'],
                        selectbackground = colors['black'],
                        selectforeground = colors['green'])
                listbox.place(x = 460, y = 35, anchor = tk.NW)
                father.listbox = listbox


                fileButton = tk.Button(frame, text = "File",
                        bd = 0, highlightbackground=colors['black'],
                        command = lambda : self.uploadFile(father.socket,
                        nameLabel))
                fileButton.place(x = 480, y = 180, anchor = tk.CENTER)
                videoButton = tk.Button(frame, text = "Video",
                        bd = 0, highlightbackground=colors['black'],
                        command = lambda : self.videoCall(father.socket,
                        nameLabel))
                videoButton.place(x = 560, y = 180, anchor = tk.CENTER)
                # ttk.Style().configure("b.TButton", foreground="black", background="white")

                # style1 = ttk.Style()
                # style1.configure("BW1.TLabel", foreground="black", background="white")
                # bt_refresh = ttk.Button(f, text = "刷新列表", bd = 0, style = "BW1.TLable",command = lambda : self.refresh(father.socket))
                tk.Label(frame, text = "System Log:",
                        bg = colors['black'],fg = colors['green']).place(
                        x = 460, y = 208, anchor = tk.NW)
                logArea = tk.Text(frame, bg = colors['black'],
                        fg = colors['green'],
                        highlightbackground = colors['lightGray'], 
                        selectbackground = colors['blue'],
                        selectforeground = colors['green'],
                        width = 16, height = 7, bd = 0)
                logArea.place(x = 455, y = 233, anchor = tk.NW)
                logArea.bind('<KeyPress>', lambda x : "break")
                father.logArea = logArea

                log = ctime() + " Connection Establishment"
                logArea.insert(tk.END, log + '\n\n')
                logArea.see(tk.END)
                # input
                nameLabel = tk.Label(frame, text = "Unseleted",
                        bg = colors['black'], fg = colors['green'],
                        width = 8)
                nameLabel.place(x = 12, y = 360)
                listbox.bind('<Double-Button-1>',
                        lambda x : self.changeSendTo(listbox, nameLabel))
                self.nameLabel = nameLabel
                inputEntry = tk.Entry(frame, width = 37,
                        bg = colors['black'], fg = colors['green'],
                        insertbackground = colors['white'],
                        highlightbackground = colors['lightGray'],
                        selectbackground = colors['blue'],
                        selectforeground = colors['green'])
                inputEntry.place(x = 90, y = 358)
                # inputEntry.bind('<Key-Return>',
                #         lambda x : self.requestCertificate(father.socket,
                #         nameLabel, inputEntry))
                inputEntry.bind('<Key-Return>',
                        lambda x : self.requestCertificate(father.socket,
                        nameLabel))
                # self.inputEntry = inputEntry
                father.inputEntry = inputEntry


                bt_send = tk.Button(frame, text = "Enter",
                        highlightbackground=colors['black'],
                        command = lambda : self.requestCertificate(father.socket,
                        nameLabel))
                bt_send.place(x = 480, y = 371, anchor = tk.CENTER)
                bt_clear = tk.Button(frame, text = "Clear",
                        highlightbackground = colors['black'],
                        command = lambda : textArea.delete(0.0, tk.END))
                bt_clear.place(x = 560, y = 372, anchor = tk.CENTER)
                
                
                r = RSA()
                c = Certificate(r.pubKey)
                
                c.certificateInfo['username'] = self.father.father.username
                self.father.father.selfInfo['username'] = self.father.father.username
                self.father.father.selfInfo['decryptionType'] = c.certificateInfo['encryptionType']
                self.father.father.selfInfo['pubKey'] = r.pubKey
                self.father.father.selfInfo['priKey'] = r.priKey
                self.father.father.selfInfo['communicationType'] = c.certificateInfo['communicationType']
                if c.certificateInfo['communicationType'] == "dh":
                    pubNum = DH().getPAndG()
                    self.father.father.selfInfo['pAndg'] = pubNum
                    c.certificateInfo['pAndg'] = pubNum
                    self.father.father.selfInfo['secretA'] = getPrimeNum(20)
                    self.father.father.selfInfo['mA'] = pow(pubNum[1],
                            self.father.father.selfInfo['secretA'], pubNum[0])


                jData = json.dumps(c.certificateInfo)
                father.socket.send(jData.encode())
                
                # 刷新列表
                # self.refresh(father.socket)

                inputEntry.focus_set()
                
                chatroom.focus_force()
                chatroom.mainloop()

                father.socket.shutdown(2)
                print ('Socket 断开')

        def __main__(self):
            # 开启监听线程
            listenThread = self.ListenThread(self.socket, self)
            listenThread.start()
            self.listenThread = listenThread


            # 建立窗口
            window = self.Window(self)
            window.__main__()
            self.window = window

    def __main__(self):
        #pass
        login = Client.Login(self)
        login.__main__()

if __name__ == '__main__':
    global HOST
    global PORT
    global BUFSIZ
    global ADDR

    HOST = 'localhost'
    PORT = 8999
    BUFSIZ = 50*1024
    ADDR = (HOST, PORT)
    MYTTL = 255

    client = Client()
    client.__main__()
