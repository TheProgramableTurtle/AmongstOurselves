# payload.py - Created by TheProgramableTurtle - 20/11/2020


class Payload:
    def __init__(self, payload):
        self.payload = payload
        self.byte = 0

    def seekFirstByte(self):
        self.byte = 0

    def seekByte(self, byte):
        self.byte = byte

    def readBytes(self, num_bytes=0, offset=0):
        if offset:
            pos = offset
        else:
            pos = self.byte

        if not num_bytes:
            ret = self.payload[pos:len(self.payload)]

            if not offset:
                self.byte = len(self.payload)

            return ret

        ret = self.payload[pos:pos + num_bytes]

        if not offset:
            self.byte += num_bytes

        return ret
