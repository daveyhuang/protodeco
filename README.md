## Usage

```python
from protodeco import loads_proto, dumps_proto
from YOUR_PROTO_pb2 improt MESSAGE

@dumps_proto(MESSAGE)
class Foo(object):
    # property & methods
    pass

f = Foo()

# now ,f have two methods: 
#    to_proto: output the filled MESSAGE, you can modify it
#    dumps_proto: serialized string.


message_str = f.dumps_proto()


@loads_proto(message_str, MESSAGE)
class Bar(object):
    pass

b = Bar()
# now, b has the property passed by message_str

```


## Notice

test 文件夹中的 proto 定义只是 用来测试 消息嵌套 的。
在实际情况中应该避免那种 会导致 **无限嵌套** 的定义
