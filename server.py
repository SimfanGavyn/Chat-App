from socket import *
from time import ctime
import threading
import json

global HOST
global PORT
global BUFSIZ
global ADDR

class User():
    def __init__(self, address, tcpCliSock):
        self.address = address
        self.tcpCliSock = tcpCliSock

class Handle():
    usernames = {} # user: usernames
    certificateInfos = {} # user: certificateInfo

    def __init__(self, user):
        self.user = user

    @staticmethod
    def getUser(username):
        def getKey(list, value):
            return [k for k,v in list.items() if v == value][0]
        return getKey(Handle.usernames, username)

    @staticmethod
    def delUsername(username):
        try:
            user = Handle.getUser(username)
            Handle.delUser(user)
        except:
            pass

    @staticmethod
    def delUser(user):
        try:
            Handle.usernames.pop(user)
            Handle.certificateInfos.pop(user)
        except Exception as e:
            print (e)

    @staticmethod
    def sendSocketToUsers(userList, data, mod = 1):
        jData = json.dumps(data)
        for user in userList:
            if mod == 1:
                user.tcpCliSock.send(jData.encode())
            else:
                user.tcpCliSock.sendall(jData.encode())
        print ("__sendToUserList__" + jData)

    @staticmethod
    def sendSocketToNames(usernameList, data, mod = 1):
        """向用户列表发送相同的数据包"""
        def getKeys(list, valueList):
            return [k for k,v in list.items() if v in valueList]
        userList = getKeys(Handle.usernames, usernameList)
        if mod == 1:
            Handle.sendSocketToUsers(userList, data)
        else:
            Handle.sendSocketToUsers(userList, data, mod)

    def sendSocketToMe(self, data):
        """给本用户发送信息包"""
        jData = json.dumps(data)
        self.user.tcpCliSock.send(jData.encode())
        print ('__send__' + jData)

    def signUp(self, data):
        """signup package"""
        with open('resource/userInfo.txt', 'r') as f:
            userJData = f.read()
            # userJData is not empty
            if userJData:
                userData = json.loads(userJData)
                if data['username'] in userData:
                    data['info'] = "SIGN UP ERROR: This username has been used."
                    data['status'] = False
                else:
                    with open('resource/userInfo.txt', 'w') as f:
                        userData[data['username']] = data['password']
                        userJData = json.dumps(userData)
                        f.write(userJData)
                    data['status'] = True
                    Handle.usernames[self.user] = data['username']
            # userJData is empty
            else:
                with open('resource/userInfo.txt', 'w') as f:
                    userData = {data['username']: data['password']}
                    userJData = json.dumps(userData)
                    f.write(userJData)
                data['status'] = True
                Handle.usernames[self.user] = data['username']
        self.sendSocketToMe(data)

    def login(self, data):
        """login package"""
        with open('resource/userInfo.txt', 'r') as f:
            userJData = f.read()
            # userJData is not empty
            if userJData:
                userData = json.loads(userJData)
                if data['username'] in userData:
                    # verify username and password
                    if userData[data['username']] == data['password']:
                        # already login
                        if self.user in Handle.usernames.keys():
                            data['info'] = "LOGIN ERROR: This port is being used."
                            data['status'] = False
                        # username in use
                        elif data['username'] in Handle.usernames.values():
                            data['info'] = "LOGIN ERROR: This username is being used."
                            data['status'] = False
                        else:
                            data['status'] = True
                            Handle.usernames[self.user] = data['username']
                    else:
                        data['info'] = 'VERIFY ERROR: Incorrect password.'
                        data['status'] = False
                else:
                    data['info'] = 'SIGN UP ERROR: You have not signed up.'
                    data['status'] = False
            # userJData is empty
            else:
                data['info'] = 'SIGN UP ERROR: You have not signed up.'
                data['status'] = False
        self.sendSocketToMe(data)



    def getCertificate(self, data):
        Handle.certificateInfos[self.user] = data
        # data['type'] = 'log'
        # data['log'] = 'Connection Establishment'
        # self.sendSocketToMe(data)
        # data = {"type": "list"}
        self.list({'type': 'list'})

    def returnCertificate(self, data):
        # print(1)
        data['type'] = 'returnCertificate'
        # print(data['to'])
        owner = Handle.getUser(data['to'])
        # print(3)
        data['certificate'] = Handle.certificateInfos[owner]
        if data['certificate']['communicationType'] == 'dh':
            data['type'] = 'communicate'
        # print(4)
        self.sendSocketToMe(data)

    def list(self, data):
        """获取在线用户列表"""
        nameList = Handle.usernames.values()
        data['list'] = list(nameList)
        print(data)
        # self.sendSocketToMe(data)
        # self.sendSocketToUsers(data)
        userList = [user for user in Handle.usernames]
        self.sendSocketToUsers(userList, data)

    def comminicate(self, data):
        toUsername = data['to']
        self.sendSocketToNames([toUsername], data)

    def singleChat(self, data):
        """私聊"""
        toUsername = data['to']
        data['senderPubKey'] = Handle.certificateInfos[Handle.getUser(data['from'])]['publicKey']
        if data.__contains__('mA'):
            data['type'] = 'returnCertificate'
        self.sendSocketToNames([toUsername], data)

    def sFile(self, data):
        toUsername = data['to']
        # data['senderPubKey'] = Handle.certificateInfos[Handle.getUser(data['from'])]['publicKey']
        self.sendSocketToNames([toUsername], data)

    def sVideo(self, data):
        toUsername = data['to']
        # data['senderPubKey'] = Handle.certificateInfos[Handle.getUser(data['from'])]['publicKey']
        self.sendSocketToNames([toUsername], data)

    def logout(self, data):
        """登出"""
        print ("用户"+ Handle.usernames[self.user] +"登出")
        Handle.delUser(self.user)

    def __main__(self, data):
        """处理信息包"""
        type = data['type']
        switch = {
            "login": self.login,
            "signup": self.signUp,
            "certificate": self.getCertificate,
            "requestCertificate": self.returnCertificate,
            "communicate": self.comminicate,
            "list": self.list,
            "singleChat": self.singleChat,
            # "groupChat": self.groupChat,
            "logout": self.logout,
            "file": self.sFile,
            "video": self.sVideo
        }
        try:
            return switch[type](data)
        except Exception as e:
            print (e)
            data['status'] = False
            data['info'] = "未知错误"
            return data

class ClientThread(threading.Thread):
    def __init__(self, user):
        threading.Thread.__init__(self)
        self.user = user

    def run(self):
        try:
            handle = Handle(self.user) # handle input
            while True:
                jData = self.user.tcpCliSock.recv(BUFSIZ).decode()
                data = json.loads(jData)
                print ("___receive___" + jData)
                if data['type'] == 'logout':
                    break
                else:
                    handle.__main__(data)
        except Exception as e:
            print ("Connection Interrupt")
            # print (e)
        finally:
            # TODO
            if self.user not in Handle.usernames:
                print ("Detected an unauthenticated user quit.")
            else:
                name = Handle.usernames[self.user]
                print ("User: "+ str(name) +" logout.")
                Handle.delUser(self.user)
                Handle.list(Handle, {"type": "list", "info": "logout"})
                # data = {"type": "list"}
            self.user.tcpCliSock.close()

    def stop(self):
        try:
            self.user.tcpCliSock.shutdown(2)
            self.user.tcpCliSock.close()
        except:
            pass

class Server():
    def __main__(self):
        tcpSerSock = socket(AF_INET, SOCK_STREAM)
        tcpSerSock.bind(ADDR)
        tcpSerSock.listen(5)

        threads = []

        while True:
            try:
                print ('Waiting for connection...')
                tcpCliSock, addr = tcpSerSock.accept()
                print ('...connected from:', addr)

                user = User(addr, tcpCliSock)
                clientThread = ClientThread(user)
                threads += [clientThread]
                clientThread.start()
            except KeyboardInterrupt:
                print ('KeyboardInterrupt:')
                for t in threads:
                    t.stop()
                break

        tcpSerSock.close()

if __name__ == '__main__':
    HOST = ''
    PORT = 8999
    BUFSIZ = 50*1024
    ADDR = (HOST, PORT)

    server = Server()
    server.__main__()
