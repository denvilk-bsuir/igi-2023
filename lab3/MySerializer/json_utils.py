from MySerializer.constants import PRIMITIVES,COLLECTIONS
from MySerializer.pack_utils import pack
from MySerializer.unpack_utils import unpack

class Json:
    def __init__(self):
        self.pos = 0
        self.indent = 0

    def dump(self, obj, fp):
        fp.write(self.dumps(obj))

    def dumps(self, obj):
        return self.serialize_to_str(pack(obj))

    def serialize_to_str(self, obj):
        if type(obj) in PRIMITIVES:
            return self.serialize_primitive(obj)

        elif type(obj) is dict:
            return self.serialize_dict(obj)
        
        elif type(obj) in COLLECTIONS:
            return self.serialize_collection(obj)

        else:
            raise Exception("Unknown type to serialize")

    def serialize_collection(self, obj):
        result = '\n' + ' ' * self.indent + '{\n'
        result += ' ' * self.indent + f'"type": "{type(obj).__name__}"\n'
        result += ' ' * self.indent + '"value": ['

        self.indent += 4

        for i in obj:
            result += self.serialize_to_str(pack(i)) + ','

        if len(result) > 1 and result[-1] == ',':
            result = result[:-1]

        self.indent -= 4
        result += '\n' + ' ' * self.indent + ']\n' + ' ' * self.indent + '}'

        return result

    def serialize_primitive(self, obj):
        result = '\n' + ' ' * self.indent + '{\n'
        result += ' ' * self.indent + f'"type": "{type(obj).__name__}"\n'
        result += ' ' * self.indent + '"value": '

        if obj is None:
            result += 'null'

        elif isinstance(obj, bool):
            result += 'true' if obj else 'false'

        elif isinstance(obj, (int, float)):
            result += str(obj)

        elif isinstance(obj, str):
            result += f'"{obj}"'

        result += '\n' + ' ' * self.indent + '}'

        return result

    def serialize_dict(self, obj):
        result = '\n' + ' ' * self.indent + '{\n'
        result += ' ' * self.indent + f'"type": "{type(obj).__name__}"\n'
        result += ' ' * self.indent + '"value": {'

        self.indent += 4

        for key, value in obj.items():
            result += self.serialize_to_str(pack(key)) + ': ' + self.serialize_to_str(pack(value)) + ', \n'

        if len(result) > 1 and result[-3] == ',':
            result = result[:-3]

        result += '\n' + ' ' * self.indent + '}\n'
        self.indent -= 4
        result += ' ' * self.indent + '}'

        return result
    
    def loads(self, s):
        self.pos = 0

        return unpack(self.deserialize_from_str(s))

    def load(self, file):
        return self.loads(file.read())
    
    def deserialize_from_str(self, string):
        self.pos = string.find('"type":', self.pos)

        if self.pos != -1:
            self.pos += len('"type": ')

        if self.pos >= len(string) or self.pos == -1:
            return

        if string[self.pos:self.pos + len('"int"')] == '"int"':
            self.pos += len('"int"\n')

            return self.deserialize_num(string)

        if string[self.pos:self.pos + len('"float"')] == '"float"':
            self.pos += len('"float"\n')

            return self.deserialize_num(string)

        if string[self.pos:self.pos + len('"bool"')] == '"bool"':
            self.pos += len('"bool"\n')

            return self.deserialize_bool(string)

        if string[self.pos:self.pos + len('"NoneType"')] == '"NoneType"':
            self.pos += len('"NoneType"\n')

            return self.deserialize_null(string)

        if string[self.pos:self.pos + len('"str"')] == '"str"':
            self.pos += len('"str"\n')

            return self.deserialize_str(string)

        if string[self.pos:self.pos + len('"dict"')] == '"dict"':
            self.pos += len('"dict"\n')

            return self.deserialize_dict(string)

        if string[self.pos:self.pos + len('"list"')] == '"list"' or \
                string[self.pos:self.pos + len('"tuple"')] == '"tuple"' or \
                string[self.pos:self.pos + len('"set"')] == '"set"':

            self.pos += 1
            ind_end = string.find('"', self.pos)
            s_type = string[self.pos: ind_end]
            self.pos = ind_end + 1

            return self.deserialize_collection(string, s_type)

    def deserialize_num(self, s):
        self.pos = s.find('"value": ', self.pos) + len('"value": ')
        s_pos = self.pos

        while self.pos < len(s) and\
                (s[self.pos].isdigit() or s[self.pos] == '.'):
            self.pos += 1

        num = s[s_pos:self.pos]
        self.pos = s.find('}', self.pos) + 1

        return float(num) if '.' in str(num) else int(num)

    def deserialize_bool(self, s):
        self.pos = s.find('"value": ', self.pos) + len('"value": ')

        if s[self.pos:self.pos + 4] == "true":
            self.pos = s.find('}', self.pos) + 1

            return True

        else:
            self.pos = s.find('}', self.pos) + 1

            return False

    def deserialize_null(self, s):
        self.pos = s.find('"value": ', self.pos) + len('"value": ')
        self.pos = s.find('}', self.pos) + 1

        return None

    def deserialize_str(self, s):
        self.pos = s.find('"value": ', self.pos) + len('"value": ')

        res = ""
        self.pos += 1

        while self.pos < len(s) and s[self.pos:self.pos + 1] not in '"\n':
            res += s[self.pos]
            self.pos += 1

        self.pos = s.find('}', self.pos) + 1

        return res

    def deserialize_dict(self, s):
        self.pos = s.find('"value": ', self.pos) + len('"value": ')
        res = {}

        self.pos += 1

        while self.pos < len(s) and s[self.pos] != '}':
            if s[self.pos] in (' ', ',', ':', '\n'):
                self.pos += 1
                continue

            k = self.deserialize_from_str(s)
            v = self.deserialize_from_str(s)
            res[k] = v

        self.pos = s.find('}', self.pos + 1) + 1

        return res

    def deserialize_collection(self, s, s_type):
        self.pos = s.find('"value": ', self.pos) + len('"value": ')

        res = []
        self.pos += 1

        while self.pos < len(s) and s[self.pos] != ']':
            if s[self.pos] in (' ', ',', '\n'):
                self.pos += 1
                continue

            v = self.deserialize_from_str(s)
            res.append(v)

        self.pos = s.find('}', self.pos) + 1

        if s_type == 'tuple':
            return tuple(res)

        elif s_type == 'set':
            return set(res)

        return res
