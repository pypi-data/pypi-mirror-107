# blackholepy

## install
```bash
pip install blackholepy
```

## example
```python
from blackholepy import client, message
import time

if __name__ == '__main__':
    c = client.Client('127.0.0.1', 12345)
    c.connect()

    # create topic
    print(c.createtopic(b't1'))
    print(c.createtopic(b't2'))
    print(c.createtopic(b't3'))

    # publish values
    # default key_type = SYSTEMTIME
    err = c.put(b't1', b'v1')
    print(err)
    err = c.put(b't2', b'v2')
    print(err)

    # user defined key-value
    err = c.put(b't3', b'v3', message.KEYTYPE_USERDEFINED, b'k3')
    print(err)

    # get values
    val = c.get(b't3', message.KEYTYPE_USERDEFINED, b'k3')
    print(val)

    # subscribe
    def handler1(msubsret):
        print("handler1: ", msubsret)

    def handler2(msubsret):
        print("handler2: ", msubsret)

    c.subs(b't1', handler1, message.KEYTYPE_BEGIN)
    c.subs(b't2', handler2, message.KEYTYPE_END)

    c2 = client.Client('127.0.0.1', 12345)
    c2.connect()
    for i in range(1000):
        c2.put(b't1', bytes(str(i), encoding='utf-8'))
        time.sleep(1)
        c2.put(b't2', bytes(str(i), encoding='utf-8'))
        time.sleep(1)

```