import socket
import threading
import time
from . import message


class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = None

        self.recv_buf = bytearray()

        self.subsmod = False
        self.subshandlers = {}

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(None)
        self.sock.connect((self.host, self.port))

    def close(self):
        self.sock.close()

    def send(self, msg):
        buf = msg.encode()
        total_size, size = len(buf), 0
        while size < total_size:
            size += self.sock.send(buf)

    def recv(self, msg):
        while True:
            ms = msg.decode(self.recv_buf)
            if ms == 0:
                self.recv_buf += self.sock.recv(1024)
                continue
            elif ms > 0:
                self.recv_buf = self.recv_buf[ms:]
                break
            else:
                raise Exception("bad message")

    def createtopic(self, topic: bytes):
        mcreatetopic = message.CreateTopic(topic)
        mcreatetopicret = message.CreateTopicRet()
        self.send(mcreatetopic)
        self.recv(mcreatetopicret)
        return mcreatetopicret.get_field('error')

    def put(self, topic: bytes, value: bytes, key_type: int = 0, key: bytes = b''):
        mput = message.Put(topic, key_type, key, value)
        mputret = message.PutRet()
        self.send(mput)
        self.recv(mputret)
        return mputret.get_field('error')

    def get(self, topic: bytes, key_type: int = 2, key: bytes = b''):
        mget = message.Get(topic, key_type, key)
        mgetret = message.GetRet()
        self.send(mget)
        self.recv(mgetret)
        return mgetret

    def subsrecv(self):
        while True:
            if self.subsmod:
                msubsret = message.SubsRet()
                self.recv(msubsret)
                topic = bytes(msubsret.get_field('topic'))
                if topic in self.subshandlers:
                    self.subshandlers[topic](msubsret)
            else:
                time.sleep(0.1)

    def subs(self, topic: bytes, handler, key_type: int = message.KEYTYPE_BEGIN, key: bytes = b''):
        self.subshandlers[topic] = handler
        if not self.subsmod:
            self.subsmod = True
            t1 = threading.Thread(target=self.subsrecv)
            t1.start()

        msubs = message.Subs(topic, key_type, key)
        self.send(msubs)


if __name__ == '__main__':
    client = Client('127.0.0.1', 12345)
    client.connect()
    createtopic = message.CreateTopic(b't01')
    createtopicret = message.CreateTopicRet()

    client.send(createtopic)
    client.recv(createtopicret)
    print("done")
