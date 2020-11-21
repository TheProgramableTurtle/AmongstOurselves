# server.py - Created by TheProgramableTurtle - 20/11/2020


class ServerHandler:
    def __init__(self, sock):
        self.clientDict = {}
        self.sock = sock

    def registerNewClient(self, packet):
        for client in self.clientDict:
            if client == packet.src_addr:
                return 1

        client = Client(packet.src_addr)
        self.clientDict[packet.src_addr] = client


class Client:
    def __init__(self, addr):
        self.addr = addr
