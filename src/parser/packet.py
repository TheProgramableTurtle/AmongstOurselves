# packet.py - Created by TheProgramableTurtle - 20/11/2020
from src.common import *
from src.parser import payload
from src.parser import packed


class Packet:
    opcode = None
    nonce = None
    data = None

    def __init__(self, recv_time, src_addr, packet_payload):
        self.recv_time = recv_time
        self.src_addr = src_addr
        self.payload = payload.Payload(packet_payload)

    def decode(self):
        self.opcode = int(self.payload.readBytes(1).hex(), 16)

        if self.opcode == PacketID.Unreliable:
            self.decodeUnreliable()
        elif self.opcode == PacketID.Reliable:
            self.decodeReliable()
        elif self.opcode == PacketID.Hello:
            self.decodeHello()
        elif self.opcode == PacketID.Disconnect:
            self.decodeDisconnect()
        elif self.opcode == PacketID.Acknowledge:
            self.decodeAcknowledge()
        elif self.opcode == PacketID.Ping:
            self.decodePing()
        else:
            sys.exit(2)

        return

    def decodeUnreliable(self):
        length = self.payload.readBytes(2)
        payloadID = self.payload.readBytes(1)
        data = self.payload.readBytes()

        self.data = {
            "length": length,
            "payloadID": payloadID,
            "data": data
        }

    def decodeReliable(self):
        nonce = self.payload.readBytes(2)
        length = self.payload.readBytes(2)
        payloadID = self.payload.readBytes(1)
        data = self.payload.readBytes()

        self.data = {
            "nonce": nonce,
            "length": length,
            "payloadID": payloadID,
            "data": data
        }

        self.nonce = nonce

    def decodeHello(self):
        nonce = self.payload.readBytes(2)
        hazelVer = self.payload.readBytes(1)
        clientVer = self.payload.readBytes(4)
        usernameLen = packed.PackedInt(self.payload.payload, self.payload.byte).decoded
        # usernameLen = self.payload.readBytes(1)
        username = self.payload.readBytes()

        self.data = {
            "nonce": nonce,
            "hazelVer": hazelVer,
            "clientVer": clientVer,
            "usernameLen": usernameLen,
            "username": username
        }

        self.nonce = nonce

    def decodeDisconnect(self):
        self.payload.readBytes(1)
        length = self.payload.readBytes(2)
        self.payload.readBytes(1)
        reason = self.payload.readBytes(1)
        message = self.payload.readBytes()

        self.data = {
            "length": length,
            "reason": reason,
            "message": message
        }

    def decodeAcknowledge(self):
        nonce = self.payload.readBytes(2)
        missing = self.payload.readBytes(1)

        self.data = {
            "nonce": nonce,
            "missing": missing
        }

        self.nonce = nonce

    def decodePing(self):
        nonce = self.payload.readBytes(2)

        self.data = {
            "nonce": nonce
        }

        self.nonce = nonce


class PacketHandler:
    def __init__(self, sock):
        self.clientDict = {}
        self.sock = sock

    def displayIncomingPacket(self, packet):
        print(f"DATA: {packet.payload}")

    def acknowledgePacket(self, packet):
        print(f"ACK: {packet.nonce}")
        data = b'\x0a' + packet.nonce + b'\xFF'
        self.sock.sendto(data, packet.src_addr)
