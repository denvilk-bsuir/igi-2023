from MySerializer.constants import PRIMITIVES,COLLECTIONS
from MySerializer.pack_utils import pack
from MySerializer.unpack_utils import unpack


class Xml:
    def __init__(self):
        self.pos = 0
        self.indent = 0

    def dumps(self, obj):
        return self.serialize_to_str(pack(obj))

    def dump(self, obj, file):
        file.write(self.dumps(obj))

    def serialize_to_str(self, obj):
        if type(obj) in PRIMITIVES:
            return self.serialize_primitive(obj)

        elif type(obj) is dict:
            return self.serialize_dict(obj)
        
        elif type(obj) in COLLECTIONS:
            return self.serialize_collection(obj)

        else:
            raise Exception("Unknown type to serialize")


    def serialize_dict(self, obj):
        result = f'<"{type(obj).__name__}">\n'
        self.indent += 4

        for key, value in obj.items():
            result += ' ' * self.indent + f'<{self.serialize_to_str(pack(key))}>\n'
            self.indent += 4
            result += ' ' * self.indent + f'{self.serialize_to_str(pack(value))}' + '\n'
            self.indent -= 4
            result += ' ' * self.indent + f'</{type(key).__name__}>' + '\n'

        if len(result) > 1 and result[-3] == ',':
            result = result[:-3]

        self.indent -= 4
        result += ' ' * self.indent + f'</"{type(obj).__name__}">'

        return result

    def serialize_primitive(self, obj):
        result = ''

        if obj is None:
            result += f'<"{type(obj).__name__}">' + 'null' + f'</"{type(obj).__name__}">'

        elif isinstance(obj, bool):
            result += f'<"{type(obj).__name__}">' + 'true' + f'</"{type(obj).__name__}">' if obj\
                else f'<"{type(obj).__name__}">' + 'false' + f'</"{type(obj).__name__}">'

        elif isinstance(obj, (int, float)):
            result += f'<"{type(obj).__name__}">' + str(obj) + f'</"{type(obj).__name__}">'

        elif isinstance(obj, str):
            result += f'<"{type(obj).__name__}">' + f'{obj}' + f'</"{type(obj).__name__}">'

        return result

    def serialize_collection(self, obj):
        result = f'<"{type(obj).__name__}">\n'
        self.indent += 4

        for i in obj:
                result += ' ' * self.indent + f'{self.serialize_to_str(pack(i))}\n'

        self.indent -= 4
        result += ' ' * self.indent + f'</"{type(obj).__name__}">'

        return result

    def loads(self, s):
        self.pos = 0
        return unpack(self.deserialize_from_str(s))

    def load(self, file):
        return self.loads(file.read())

    def deserialize_from_str(self, string):
        self.pos = string.find('<"', self.pos)

        if self.pos != -1:
            self.pos += len('<')  

        if self.pos >= len(string) or self.pos == -1:
            return None

        if string[self.pos:self.pos + len('"int"')] == '"int"':
            self.pos += len('"int"')

            return self.deserialize_num(string)

        if string[self.pos:self.pos + len('"float"')] == '"float"':
            self.pos += len('"float"')

            return self.deserialize_num(string)

        if string[self.pos:self.pos + len('"bool"')] == '"bool"':
            self.pos += len('"bool"')

            return self.deserialize_bool(string)

        if string[self.pos:self.pos + len('"NoneType"')] == '"NoneType"':
            self.pos += len('"NoneType"')

            return self._deserialize_null(string)

        if string[self.pos:self.pos + len('"str"')] == '"str"':
            self.pos += len('"str"')

            return self.deserialize_str(string)

        if string[self.pos:self.pos + len('"dict"')] == '"dict"':
            self.pos += len('"dict"')
            return self.deserialize_dict(string)

        if string[self.pos:self.pos + len('"list"')] == '"list"' or \
                string[self.pos:self.pos + len('"tuple"')] == '"tuple"' or \
                string[self.pos:self.pos + len('"set"')] == '"set"':

            self.pos += 1
            ind_end = string.find('"', self.pos)
            s_type = string[self.pos: ind_end]
            self.pos = ind_end + 2

            return self.deserialize_collection(string, s_type)

    def deserialize_num(self, s):
        self.pos = s.find('>', self.pos) + len('>')
        s_pos = self.pos

        while self.pos < len(s) and\
                ((s[self.pos].isdigit() or s[self.pos] == '.') and s[self.pos] != '<'):
            self.pos += 1

        num = s[s_pos:self.pos]
        self.pos = s.find('>', self.pos) + 1

        return float(num) if '.' in str(num) else int(num)

    def deserialize_collection(self, s, s_type):
        res = []
        self.pos = s.find('<', self.pos + 1)
        while self.pos < len(s) and\
                s[self.pos: self.pos + len(s_type) + 5] != f'</"{s_type}">':

            v = self.deserialize_from_str(s)
            res.append(v)
            self.pos = s.find('<', self.pos)

        if s_type == 'tuple':
            self.pos += 1
            return tuple(res)

        elif s_type == 'set':
            self.pos += 1
            return set(res)
        else:
            self.pos += 1
            return res

    def deserialize_dict(self, s):
        res = {}

        while self.pos < len(s) and s[self.pos:self.pos+len('</"dict">')] != '</"dict">':
            self.pos = s.find('<', self.pos)

            while s[self.pos+1] == '/' and s[self.pos:self.pos+9] != '</"dict">':
                self.pos = s.find('<', self.pos+1)
            if s[self.pos+1] == '/' and s[self.pos:self.pos+9] == '</"dict">':
                self.pos = s.find('<', self.pos + 1)
                return res
            k = self.deserialize_from_str(s)
            v = self.deserialize_from_str(s)

            res[k] = v

            if self.pos == -1:
                return res

        return res

    def deserialize_str(self, s):
        res = ''
        self.pos = s.find('>', self.pos) + 1

        while self.pos < len(s) and s[self.pos] != '<':
            res += s[self.pos]
            self.pos += 1

        self.pos = s.find('>', self.pos)
        return res

    def deserialize_bool(self, s):
        self.pos = s.find('>', self.pos) + len('>')

        if s[self.pos:self.pos + 4] == "true":
            self.pos = s.find('>', self.pos) + 1
            return True

        else:
            self.pos = s.find('>', self.pos) + 1
            return False

    def _deserialize_null(self, s):
        self.pos = s.find('>', self.pos) + len('>')
        self.pos = s.find('>', self.pos) + 1

        return None