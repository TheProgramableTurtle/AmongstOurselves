# payload.py - Created for Ejected by TheProgramableTurtle, Pr0x1mas and coder-carvey - 20/11/2020


class Payload:
    def __init__(self, payload):
        self.payload = payload
        self.byte = 0

    def seekFirstByte(self):
        self.byte = 0

    def seekByte(self, byte):
        self.byte = byte

    def readBytes(self, num_bytes=0):
        if not num_bytes:
            ret = self.payload[self.byte:len(self.payload)]
            self.byte = len(self.payload)

            return ret

        ret = self.payload[self.byte:self.byte + num_bytes]
        self.byte += num_bytes

        return ret
