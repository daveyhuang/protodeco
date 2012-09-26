# -*- coding:utf-8 -*-

import os
import sys

CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
PROJECT_PATH = os.path.dirname(CURRENT_PATH)
sys.path.append(PROJECT_PATH)

from protodeco import loads_proto, dumps_proto

from msg.person_pb2 import Person as ProtoPerson
from msg.pets_pb2 import Pets as ProtoPets, Food as ProtoFood



############################################
# Test Data

class Food(object):
    pass
class Pets(object):
    pass

aa = Food()
aa.name = 'aa'
aa.price = 120

bb = Food()
bb.name = 'bb'

hehe = Pets()
hehe.kind = ProtoPets.DOG
hehe.name = 'hehe'
hehe.favorite_food = [aa, bb]

gaga = Pets()
gaga.kind = ProtoPets.CAT
gaga.name = 'gaga'

huahua = Pets()
huahua.kind = ProtoPets.DOG
huahua.favorite_food = [bb]






############################################
#
#   dumps_proto 数据到消息的转换
#
############################################


# 在数据类上加上 dumps_proto 的装饰器，
# 参数是要 dumps 的 message type
# 这样就会自动在这个类的实例上加上 
# to_proto, dumps_proto 这两个方法

@dumps_proto(ProtoPerson)
class Person(object):
    pass


############################################
# test data
lilei = Person()
lilei.name = 'lilei'
lilei.age = 25
lilei.pets = [hehe, gaga, huahua]
lilei.words = ['wo shi lilei', 'wo ai hanmeimei']
lilei.value = 'LILEI'

hanmeimei = Person()
hanmeimei.name = 'hanmeimei'
hanmeimei.age = 24
hanmeimei.pets = [gaga, huahua]
hanmeimei.words = ['a ya', 'lun jia']

lilei.friends = [hanmeimei]
############################################



print lilei.to_proto()

message_str = lilei.dumps_proto()


############################################
#
#   loads_proto 消息到数据的转换 
#
############################################


# 在数据类上加上 loads_proto 的装饰器，
# 参数是接收到的message_str和message type
# 这样就会自动在类的实例上添加上消息中的属性

@loads_proto(message_str, ProtoPerson)
class NewPerson(object):
    pass

np = NewPerson()


print np.name, np.age, np.words, np.value
print np.friends
print np.pets
for f in np.friends:
    print f.name, f.age, f.words, f.friends, f.pets, f.value
print
for p in np.pets:
    print p.name, p.kind, p.favorite_food
    for fd in p.favorite_food:
        print fd.name, fd.price
