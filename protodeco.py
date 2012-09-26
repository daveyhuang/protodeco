# -*-coding:utf-8 -*-


def loads_proto(message_str, proto_type):
    """
    Param: message_str, 序列化后的string
    Param: proto_type, proto中定义的message
    """
    m = proto_type()
    m.ParseFromString(message_str)
    
    def deco(cls):
        def wrap(*args, **kwargs):
            instance = cls(*args, **kwargs)
            
            def loads(instance, m):
                all_fields = m.DESCRIPTOR.fields
                fields = dict(m.ListFields())

                for f in all_fields:
                    if f not in fields:
                        # 从所有的域开始历遍，遇到没填充的域，就赋值为non_value
                        non_value = [] if f.label == 3 else None
                        setattr(instance, f.name, non_value)
                        continue

                    if f.label != 3 or not f.message_type:
                        # label != 3 是非 repeated 的域
                        # message_type == None 是 proto 内置类型
                        # 对于此种属性，直接赋值即可
                        setattr(instance, f.name, fields[f])
                    else:
                        # repeated 的域，并且是自定义类型
                        # 需要递归的处理这些类型
                        class_name = f.message_type.name
                        repeated_value = []
                        for v in fields[f]:
                            _new_class = type(class_name, (object,), {})
                            loads(_new_class, v)
                            repeated_value.append(_new_class)
                        
                        setattr(instance, f.name, repeated_value)
            
            loads(instance, m)
            return instance
        return wrap
    return deco
    
    
    

def dumps_proto(proto_type):
    """
    Param: proto_type, proto中定义的message
    使用此装饰器的类，会自动添加两个方法:
    to_proto: 得到一个填充好的proto_type message，可以对此message进一步处理
    dumps_proto: 序列化后的string，其实就是 to_proto().SerializeToString()
    """
    
    def deco(cls):
        def wrap(*args, **kwargs):
            instance = cls(*args, **kwargs)
            
            def dumps(instance, m):
                fields = [(f.name, f.label, f.message_type) for f in m.DESCRIPTOR.fields]
                
                for name, label, message_type in fields:
                    if label == 2:    # required
                        if not hasattr(instance, name):
                            raise Exception("{0} is required".format(name))
                        setattr(m, name, getattr(instance, name))
                        
                    elif label == 3:  # repeated
                        value = getattr(instance, name, [])
                        field = getattr(m, name)
                        if not message_type:
                            # 内置类型，直接赋值
                            field.extend(value)
                        else:
                            # 自定义类型，递归处理
                            for v in value:
                                dumps(v, field.add())
                    else:   # optional
                        if hasattr(instance, name):
                            setattr(m, name, getattr(instance, name))
                return m
                            
            setattr(instance, 'to_proto', lambda: dumps(instance, proto_type()))
            setattr(instance, 'dumps_proto', lambda: dumps(instance, proto_type()).SerializeToString())
            
            return instance
        return wrap
    return deco
