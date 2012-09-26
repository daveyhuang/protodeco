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


message_str = d.dumps_proto()


@loads_proto(message_str, MESSAGE)
class Bar(object):
    pass

b = Bar()
# now, b has the property passed by message_str

```
