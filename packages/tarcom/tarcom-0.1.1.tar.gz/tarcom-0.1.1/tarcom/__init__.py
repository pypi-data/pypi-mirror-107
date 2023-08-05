# Programmer: Tarek Darghouth Moghrabi
# Created: 2019, 4, 24, 18: 13

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files(the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and / or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


import os
import time
import threading
import socket
import asyncore

# NetworkCom: Tcp server and client.


class NetworkCom:
    @property
    def networkType(self):
        return self._networkType

    @networkType.setter
    def networkType(self, value):
        self._networkType = value

    @property
    def connected(self):
        return self._connected

    @connected.setter
    def connected(self, value):
        self._connected = value

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, value):
        self._address = value

    @property
    def name(self):
        return self._name

    @property
    def ipLocal(self):
        return self._ipLocal

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, value):
        self._port = value

    @property
    def connectionUpdated(self):
        return self._connectionUpdated

    @connectionUpdated.setter
    def connectionUpdated(self, value):
        self._connectionUpdated.removeAt(0)
        self._connectionUpdated.append(value)

    @property
    def dataReceived(self):
        return self._dataReceived

    @dataReceived.setter
    def dataReceived(self, value):
        self._dataReceived.removeAt(0)
        self._dataReceived.append(value)

    @property
    def dataCurrent(self):
        return self._dataCurrent
    _networkType = 0
    _connected = False
    _address = None
    _name = None
    _ipLocal = None
    _dataCurrent = None
    __tcp = None

    def __init__(self, networkType, port, address=""):
        self._networkType = networkType

        if port < 0 or networkType > 1:
            raise Exception(
                "Network type should be [0] for server or [1] for client.")

        self._connected = False
        self._address = address
        self._ipLocal = NetworkCom.getLocalIP(address)

        if port > 65535:
            raise Exception("Port should be smaller than 65535.")
        if port <= 0:
            raise Exception("Port should be bigger than 0.")
        self._port = port
        self.checkConnect()
        self._connectionUpdated = Event()
        self._connectionUpdated()
        self._dataReceived = Event()
        self._dataReceived()

    @staticmethod
    def getLocalIP(address):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect((address, 1))
            IP = s.getsockname()[0]
        except:
            try:
                s.connect(('10.255.255.255', 1))
                IP = s.getsockname()[0]
            except:
                IP = ''
        finally:
            s.close()
        return IP

    def connectionUpdatedHandler(self, args):
        if self._networkType == 0:
            self.connected = args.connected
            self.connectionUpdated(self, args)
        elif self._networkType == 1:
            if self.connected != args.connected:
                self.connected = args.connected
                self.connectionUpdated(self, args)

    def dataReceivedHandler(self, args):
        self._dataCurrent = args.data
        self.dataReceived(self, args)

    def connect(self):
        isAsync = True
        if isAsync:
            self.__tcp = AsyncoreSocketTCP(
                self.networkType, self.ipLocal, self.address, self._port)
            self.__tcp.isCheck = True
            self.__tcp.connUpdatedEvent.append(self.connectionUpdatedHandler)
            self.__tcp.dataRcvEvent.append(self.dataReceivedHandler)
            self.checkConnect()
            loop_thread = threading.Thread(
                target=asyncore.loop, name="Asyncore Loop")
            loop_thread.daemon = True
            loop_thread.start()
        else:
            self.__tcp = TCP(self.ipLocal, self.address, self._port)
            self.__tcp.start()
            while True:
                time.sleep(0.001)
                self.__tcp.receive()
                if self.__tcp.data is not None:
                    self.__tcp.data = None

    def checkConnect(self):
        pass

    def send(self, msg):
        self.__tcp.send(msg)

    def close(self):
        self.connected = False
        self.__tcp.close()


class TCP:
    Connected = False
    ipLocal = None
    ipRemote = None
    port = -1
    data = None
    sock = None
    dataRcvEvent = None

    def __init__(self, ipLocal, ipRemote, port):
        self.ipLocal = ipLocal
        self.ipRemote = ipRemote
        self.port = port
        self.dataRcvEvent = Event()
        self.dataRcvEvent()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setblocking(False)

    def start(self):
        if self.ipLocal is None or self.ipRemote is None or self.port == -1:
            return
        while self.connected == False:
            try:
                self.sock.bind((self.ipLocal, self.port))
                break
            except:
                pass
        self.sock.sendto(b"1", (self.ipRemote, self.port))

    def receive(self):
        try:
            data, addr = self.sock.recvfrom(65000)
            if str(addr[0]) == self.ipRemote:
                self.connected = True
                self.data = data
                self.dataRcvEvent(data)
        except:
            pass

    def send(self, msg):
        try:
            self.sock.sendto(bytes(msg, 'utf-8'), (self.ipRemote, self.port))
        except:
            pass

    def stop(self):
        self.connected = False
        self.sock.close()


class AsyncoreSocketTCP(asyncore.dispatcher_with_send):
    __connected = False
    ipLocal = None
    ipRemote = list()
    __sockets = list()
    port = -1
    data = None
    dataRcvEvent = None
    connUpdatedEvent = None
    isCheck = False
    __networkType = 0
    __checkCount = 0
    __checkCountMax = 15
    __clientReadThreads = list()
    listSockets = []

    def __init__(self, networkType, ipLocal, ipRemote, port):
        self.__networkType = networkType
        self.ipLocal = ipLocal
        if os.name != "nt":
            self.ipLocal = ''
        if networkType == 1 and ipRemote != None:
            self.validateIp(ipRemote)
            self.ipRemote.append(ipRemote)
        self.port = port
        self.dataRcvEvent = Event()
        self.dataRcvEvent()
        self.connUpdatedEvent = Event()
        self.connUpdatedEvent()
        asyncore.dispatcher.__init__(self)
        self.startConnect()
        AsyncoreSocketTCP.listSockets.append(self)

    def validateIp(self, ip):
        try:
            socket.inet_aton(ip)
        except socket.error:
            raise Exception("Invalid ip " + ip)

    def startConnect(self):
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        if self.__networkType == 0:
            self.bind((self.ipLocal, self.port))
            self.listen(10)
        elif self.__networkType == 1:
            try:
                self.connect((self.ipRemote[0], self.port))
                pass
            except Exception as e:
                if e != None:
                    pass
                time.sleep(1)
                self.startConnect()
                pass

    def handle_connect_event(self):
        asyncore.dispatcher_with_send.handle_connect_event(self)
        if self.connected:
            self.__connected = True
            self.connUpdatedEvent(
                ConnectionUpdatedEventArgs(self.ipRemote[0], True))

    def handle_accepted(self, sock, addr):
        if self.ipRemote.__contains__(addr[0]):
            self.ipRemote.remove(addr[0])
            for socket in self.__sockets:
                if socket[0] == addr[0]:
                    self.__sockets.remove(socket)
                    break
            for clientReadThread in self.__clientReadThreads:
                if clientReadThread[0] == addr[0]:
                    clientReadThread[1].isClose = True
                    self.__clientReadThreads.remove(clientReadThread)
                    break

        self.ipRemote.append(addr[0])
        self.__sockets.append((addr[0], sock))
        thread = threading.Thread(
            target=self.readData, name="Client Read Loop " + addr[0], args=[addr[0], sock, True])
        thread.daemon = True
        thread.start()
        self.__clientReadThreads.append((addr[0], thread))
        self.connUpdatedEvent(ConnectionUpdatedEventArgs(addr[0], True))

    def handle_error(self):
        pass

    def handle_expt(self):
        pass

    def handle_close(self):
        pass

    def handle_read(self):
        if self.isCheck:
            self.__checkCount += 1
            if self.__checkCount >= self.__checkCountMax:
                self.__checkCount = 0
                if self.__connected:
                    if self.__networkType == 1:
                        self.connected = False
                        self.__connected = False
                        self.connUpdatedEvent(
                            ConnectionUpdatedEventArgs(self.ipRemote[0], False))
                        try:
                            self.connected = False
                            self.__connected = False
                            for ip in self.ipRemote:
                                self.connUpdatedEvent(
                                    ConnectionUpdatedEventArgs(ip, False))
                            self.socket.close()
                            asyncore.dispatcher_with_send.close(self)
                        except Exception as e:
                            if e != None:
                                pass
                        while not self.socket._closed:
                            pass
                        time.sleep(1)
                        self.startConnect()

        self.readData(self.ipRemote[0], self.socket)

    def readData(self, remoteAddress, socket, always=False):
        address = remoteAddress
        while(True):
            try:
                data, addr = socket.recvfrom(65000)
                dataCount = len(data)
                if dataCount > 0:
                    if self.__networkType == 1:
                        if not self.__connected:
                            self.__connected = True
                            self.connUpdatedEvent(
                                ConnectionUpdatedEventArgs(address, True))
                    self.__checkCount = 0
                    self.data = data
                    self.dataRcvEvent(DataReceivedEventArgs(
                        address, data.decode('utf-8')))
                else:
                    if self.isCheck:
                        self.__checkCount += 1
                        if self.__checkCount >= self.__checkCountMax:
                            self.__checkCount = 0
                            if self.__networkType == 0:
                                self.connUpdatedEvent(
                                    ConnectionUpdatedEventArgs(address, False))
                                break
            except Exception as e:
                if e != None:
                    pass
                if self.__networkType == 0:
                    self.__checkCount = 0
                pass
            if not always:
                break
            else:
                t = threading.currentThread()
                isClose = getattr(t, "isClose", False)
                if isClose:
                    break

    def writable(self):
        return True

    def readable(self):
        return True

    def send(self, msg, ip=None):
        sendIp = list()
        if ip != None:
            sendIp.append(ip)
        else:
            sendIp = self.ipRemote
        for ip in sendIp:
            if ip != None:
                try:
                    if self.__networkType == 0:
                        for socket in self.__sockets:
                            if socket[0] == ip:
                                socket[1].send(bytes(msg, 'utf-8'))
                                break
                    elif self.__networkType == 1:
                        self.socket.sendto(
                            bytes(msg, 'utf-8'), (ip, self.port))
                except Exception as e:
                    if e != None:
                        pass
                    pass

    def close(self):
        AsyncoreSocketTCP.listSockets.remove(self)
        self.connected = False
        self.__connected = False
        for ip in self.ipRemote:
            self.connUpdatedEvent(ConnectionUpdatedEventArgs(ip, False))
        # self.socket.close()
        asyncore.dispatcher_with_send.close(self)


class Event(list):
    def __call__(self, *args, **kwargs):
        for f in self:
            f(*args, **kwargs)

    def __repr__(self):
        return "Event(%s)" % list.__repr__(self)

    def removeAt(self, index):
        if index < len(self):
            self.remove(self[index])


class ConnectionUpdatedEventArgs:
    @property
    def address(self):
        return self._address

    @property
    def connected(self):
        return self._connected

    _address = None
    _connected = None

    def __init__(self, address, connected):
        self._address = address
        self._connected = connected


class DataReceivedEventArgs:
    @property
    def address(self):
        return self._address

    @property
    def data(self):
        return self._data

    _address = None
    _data = None

    def __init__(self, address, data):
        self._address = address
        self._data = data


class TcpServer(NetworkCom):
    def __init__(self, port):
        super().__init__(0, port)


class TcpClient(NetworkCom):
    def __init__(self, address, port):
        super().__init__(1, port, address)
