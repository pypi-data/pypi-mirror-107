import crcmod

KEYTYPE_SYSTEMTIME = 0
KEYTYPE_BEGIN = 1
KEYTYPE_END = 2
KEYTYPE_USERDEFINED = 3


class Coding:
    def encode_int(v, size):
        res = bytearray()
        for i in range(size):
            res.append((v >> (i*8)) & 0xff)
        return res

    def decode_int(buf, size):
        res = 0
        for i in range(size):
            res |= int(buf[i]) << (i * 8)
        return res

    def encode_string(v):
        res = bytearray()
        n = len(v)
        res += Coding.encode_int(n, 4)
        res += v
        return res

    def decode_string(buf):
        n = Coding.decode_int(buf, 4)
        return buf[4:4 + n]

    def size_int(v, size):
        return size

    def size_string(v):
        return 4 + len(v)

    def crc(v):
        crc32_func = crcmod.mkCrcFun(0x104C11DB7, initCrc=0, xorOut=0xFFFFFFFF)
        return crc32_func(v)


class Field:
    def __init__(self, name, type, child_field=None):
        self.name = name
        self.type = type
        self.child_field = child_field
        self.value = None
        if self.type == 'uint8_t':
            self.value = 0
        elif self.type == 'uint32_t':
            self.value = 0
        elif self.type == 'string':
            self.value = b''
        elif self.type == 'vector':
            self.value = []
        else:
            raise Exception("unknown type: ", type)
        self.encoding = 'utf-8'

    def size(self):
        if self.type == 'uint8_t':
            return 1

        elif self.type == 'uint32_t':
            return 4

        elif self.type == 'string':
            return 4 + len(self.value)

        elif self.type == 'vector':
            size = 4
            for v in self.value:
                self.type += v.size()
            return size
        else:
            raise Exception("unknown type: ", self.type)

    def encode(self) -> bytearray:
        res = bytearray()
        if self.type == 'uint8_t':
            res += Coding.encode_int(self.value, 1)

        elif self.type == 'uint32_t':
            res += Coding.encode_int(self.value, 4)

        elif self.type == 'string':
            res += Coding.encode_int(len(self.value), 4)
            res += self.value

        elif self.type == 'vector':
            res += Coding.encode_int(len(self.value), 4)
            for v in self.value:
                res += v.encode()
        else:
            raise Exception("unknown type: ", self.type)
        return res

    def decode(self, buf):
        if self.type == 'uint8_t':
            self.value = Coding.decode_int(buf, 1)
            return 1

        elif self.type == 'uint32_t':
            self.value = Coding.decode_int(buf, 4)
            return 4

        elif self.type == 'string':
            self.value = Coding.decode_string(buf)
            return len(self.value) + 4

        elif self.type == 'vector':
            cnt = Coding.decode_int(buf, 4)
            size = 4
            self.value = []
            for i in range(cnt):
                cf = Field(self.child_field.name,
                           self.child_field.type, self.child_field.child_field)
                size += cf.decode(buf[size:])
                self.value.append(cf)
            return size

        else:
            raise Exception("can't decode")

    def __str__(self):
        if self.type == 'vector':
            res = self.name + ': ['
            for v in self.value:
                res += str(v) + ","
            res += ']'
            return res
        else:
            return self.name + ": " + str(self.value)


class Message:
    def __init__(self):
        self.length = Field('length', 'uint32_t')
        self.name = Field('name', 'string')
        self.name.value = bytes(self.__class__.__name__, 'utf-8')
        self.crc = Field('crc', 'uint32_t')

    def encode(self):
        res = bytearray()
        size = self.size()
        self.set_field('length', size)
        res += self.length.encode()
        res += self.name.encode()
        for field in self.fields:
            res += field.encode()

        self.set_field('crc', Coding.crc(res))
        res += self.crc.encode()
        return res

    # 0: not full  -1: bad   >0: size of the msg
    def decode(self, buf):
        if len(buf) < 4:
            return 0

        size = 0
        size += self.length.decode(buf[size:])
        if self.length.value > len(buf):
            return 0

        size += self.name.decode(buf[size:])
        for field in self.fields:
            size += field.decode(buf[size:])
        size += self.crc.decode(buf[size:])

        if Coding.crc(buf[:self.length.value - 4]) != self.crc.value:
            return -1

        return size

    def get_field(self, field):
        fs = [self.length, self.name] + self.fields + [self.crc]
        for f in fs:
            if field == f.name:
                return f.value
        return None

    def set_field(self, field, value):
        fs = [self.length, self.name] + self.fields + [self.crc]
        for f in fs:
            if field == f.name:
                f.value = value
                return True
        raise Exception("no field: ", field)

    def size(self):
        fs = [self.length, self.name] + self.fields + [self.crc]
        size = 0
        for f in fs:
            size += f.size()
        return size

    def __str__(self):
        res = '{'
        fs = [self.length, self.name] + self.fields + [self.crc]
        for f in fs:
            res += f.__str__() + ", "
        res += '}'
        return res


class CreateTopic(Message):
    def __init__(self, topic: bytes = b''):
        super().__init__()
        self.fields = [Field('topic', 'string')]
        self.set_field('topic', topic)


class CreateTopicRet(Message):
    def __init__(self, error: bytes = b''):
        super().__init__()
        self.fields = [Field('error', 'string')]
        self.set_field('error', error)


class Put(Message):
    def __init__(self, topic: bytes = b'', key_type: int = 0, key: bytes = b'', value: bytes = b''):
        super().__init__()
        self.fields = [Field('topic', 'string'), Field(
            'key_type', 'uint8_t'), Field('key', 'string'), Field('value', 'string')]
        self.set_field('topic', topic)
        self.set_field('key_type', key_type)
        self.set_field('key', key)
        self.set_field('value', value)


class PutRet(Message):
    def __init__(self, error: bytes = b''):
        super().__init__()
        self.fields = [Field('error', 'string')]
        self.set_field('error', error)


class Get(Message):
    def __init__(self, topic: bytes = b'', key_type: int = 0, key: bytes = b''):
        super().__init__()
        self.fields = [Field('topic', 'string'), Field(
            'key_type', 'uint8_t'), Field('key', 'string')]
        self.set_field('topic', topic)
        self.set_field('key_type', key_type)
        self.set_field('key', key)


class GetRet(Message):
    def __init__(self, topic: bytes = b'', key: list = [], value: list = [], error: bytes = b''):
        super().__init__()
        self.fields = [Field('topic', 'string'), Field('key', 'vector', Field('', 'string')), Field(
            'value', 'vector', Field('', 'string')), Field('error', 'string')]
        self.set_field('topic', topic)
        self.set_field('key', key)
        self.set_field('value', value)
        self.set_field('error', error)


class Subs(Message):
    def __init__(self, topic: bytes = b'', key_type: int = 0, key: bytes = b''):
        super().__init__()
        self.fields = [Field('topic', 'string'), Field(
            'key_type', 'uint8_t'), Field('key', 'string')]
        self.set_field('topic', topic)
        self.set_field('key_type', key_type)
        self.set_field('key', key)


class SubsRet(Message):
    def __init__(self, topic: bytes = b'', key: bytes = b'', value: bytes = b'', error: bytes = b''):
        super().__init__()
        self.fields = [Field('topic', 'string'), Field('key', 'string'), Field(
            'value', 'string'), Field('error', 'string')]
        self.set_field('topic', topic)
        self.set_field('key', key)
        self.set_field('value', value)
        self.set_field('error', error)


if __name__ == '__main__':
    mcreatetopic = CreateTopic(b'topic01')
    me = mcreatetopic.encode()
    mcreatetopic.decode(me)
    print(mcreatetopic)

    mcreatetopicret = CreateTopicRet()
    me = mcreatetopicret.encode()
    mcreatetopicret.decode(me)
    print(mcreatetopicret)

    mput = Put()
    me = mput.encode()
    mput.decode(me)
    print(mput)

    mputret = PutRet()
    me = mputret.encode()
    mputret.decode(me)
    print(mputret)

    mget = Get()
    me = mget.encode()
    mget.decode(me)
    print(mget)

    mgetret = GetRet()
    me = mgetret.encode()
    mgetret.decode(me)
    print(mgetret)

    msubs = Subs()
    me = msubs.encode()
    msubs.decode(me)
    print(msubs)

    msubsret = SubsRet()
    me = msubsret.encode()
    msubsret.decode(me)
    print(msubsret)
