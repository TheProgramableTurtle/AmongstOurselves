# packed.py - Created by TheProgramableTurtle - 20/11/2020
from src.parser import payload


class PackedInt:
    encoded = 0
    decoded = 0

    def __init__(self, data, offset=0, is_decoded=False):
        if not is_decoded:
            self.encoded = payload.Payload(data)
            self.encoded.seekByte(offset)
            self.decode()
        else:
            self.decoded = data
            self.encode()

    def decode(self):
        shift = 0

        while True:
            byte = int(self.encoded.readBytes(1).hex(), 16)
            read = (byte >> 0x80) & 0x1
            val = byte ^ 0x80 if read else byte

            self.decoded |= val << shift

            if not read:
                break

            shift += 7

    def encode(self):
        shift = 0

        while True:
            byte = (self.decoded >> shift) & 0xFF

            if byte < 0x80:
                self.encoded |= byte << shift
                break

            byte |= 0x80
            self.encoded |= byte << shift

            shift += 7
