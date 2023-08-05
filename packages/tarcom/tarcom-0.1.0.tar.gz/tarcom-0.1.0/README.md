# TarCo Communication (tarcom)

## TcpClient
Communicate with network devices as TCP client.

## TcpServer
Create a TCP server to communicate with network devices.

&nbsp;
&nbsp;

### Usage
```python
from tarcom import TcpServer, TcpClient

print("Started")

isServer = True

address = "192.168.0.1"
port = 42424

if isServer:
    com = TcpServer(port)
else:
    com = TcpClient(address, port)


def connectionUpdatedEventHandler(sender, args):
    if(args.connected):
        print(args.address + ": " + "Connected")
    else:
        print(args.address + ": " + "Disconnected")


def dataReceivedEventHandler(sender, args):
    print(args.address + ": " + args.data)


com.connectionUpdated = connectionUpdatedEventHandler
com.dataReceived = dataReceivedEventHandler
com.connect()

inputStr = None
while inputStr != "E":
    inputStr = input("Input (E = Exit):\n")
    if inputStr != None:
        com.send(inputStr)

print("Stopped")
```

&nbsp;
&nbsp;
> **Internal Use Only** (Use at your own risk)