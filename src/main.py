# main.py - Created for Ejected by TheProgramableTurtle, Pr0x1mas, and coder-carvey - 20/11/2020

from src.common import *
from src import server
from src import packet


class ThreadMain(threading.Thread):
    def __init__(self, priority):
        threading.Thread.__init__(self)
        self.priority = priority

    def run(self):
        main()


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    addr = ('', 22023)

    sock.bind(addr)

    serverHandler = server.ServerHandler(sock)
    packetHandler = packet.PacketHandler(sock)

    while True:
        payload, addr = sock.recvfrom(4096)

        recv_packet = packet.Packet(time.time, addr, payload)

        serverHandler.registerNewClient(recv_packet)
        packetHandler.displayIncomingPacket(recv_packet.payload)

        recv_packet.decode()

        if recv_packet.nonce:
            packetHandler.acknowledgePacket(recv_packet)


if __name__ == "__main__":
    print("Starting server on Thread-1")
    threadMain = ThreadMain(1)
    threadMain.start()
