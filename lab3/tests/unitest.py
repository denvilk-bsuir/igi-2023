import unittest
from MySerializer.MySerializer import MySerializer
from tests.test_attributes import foo,gen,lam,first,rec, A,B,C,firstIn,fooMath,closure


class JsonTests(unittest.TestCase):

    def test_json_func(self):        
        ser = MySerializer.createSerializer(".json")                
        self.assertEqual(foo(2,2),ser.loads(ser.dumps(foo))(2,2))
        for i,k in zip(gen(1),ser.loads(ser.dumps(gen))(1)):
            self.assertEqual(i,k)  
        self.assertEqual(lam(1),ser.loads(ser.dumps(lam))(1))
        self.assertEqual(first(1),ser.loads(ser.dumps(first))(1))
        self.assertEqual(rec(4),ser.loads(ser.dumps(rec))(4))
        self.assertEqual(firstIn(4),ser.loads(ser.dumps(firstIn))(4))


    def test_json_primitive(self):
        ser = MySerializer.createSerializer(".json")
        obj = 1
        self.assertEqual(obj,ser.loads(ser.dumps(obj)))
        obj = True
        self.assertEqual(obj,ser.loads(ser.dumps(obj)))
        obj = "a"
        self.assertEqual(obj,ser.loads(ser.dumps(obj)))
        obj = 1.1
        self.assertEqual(obj,ser.loads(ser.dumps(obj)))
        obj = None
        self.assertEqual(obj,ser.loads(ser.dumps(obj)))

    def test_json_collections(self):
        ser = MySerializer.createSerializer(".json")
        obj = [1,2,3,4,5]
        self.assertEqual(obj,ser.loads(ser.dumps(obj)))
        obj = (1,2,3,4,5)
        self.assertEqual(obj,ser.loads(ser.dumps(obj)))
        obj = {1,2,3,4,5}
        self.assertEqual(obj,ser.loads(ser.dumps(obj)))
        obj = {1:1,2:2,3:3,4:4,5:5}
        self.assertEqual(obj,ser.loads(ser.dumps(obj)))

    def test_json_func_with_lib(self):
        ser = MySerializer.createSerializer(".json")
        self.assertEqual(fooMath(2),ser.loads(ser.dumps(fooMath))(2))


    def test_json_class(self):                     
        ser = MySerializer.createSerializer(".json")
        _class = A
        _serializedClass = ser.loads(ser.dumps(_class))

        a = _class(1)
        b = _serializedClass(1)
    
        self.assertEqual(a.num,b.num)
        self.assertEqual(a.a_var,b.a_var)
        self.assertEqual(a.a_func(),b.a_func())
        self.assertEqual(a.prop_test,b.prop_test)


    def test_json_classInheritance(self):
        ser = MySerializer.createSerializer(".json")
        _class = B
        _serializedClass = ser.loads(ser.dumps(_class))
        a = _class(1)
        b = _serializedClass(1)

        self.assertEqual(a.num,b.num)
        self.assertEqual(a.a_var,b.a_var)
        self.assertEqual(a.a_func(),b.a_func())
        self.assertEqual(a.b_func(),b.b_func())

        _class = C
        _serializedClass = ser.loads(ser.dumps(_class))
        a = _class(1)
        b = _serializedClass(1)

        self.assertEqual(a.num,b.num)
        self.assertEqual(a.a_var,b.a_var)
        self.assertEqual(a.a_func(),b.a_func())
        self.assertEqual(a.b_func(),b.b_func())
        self.assertEqual(a.letter(),b.letter())

    def test_json_object(self):
        ser = MySerializer.createSerializer(".json")
        a = B(1)
        b = ser.loads(ser.dumps(a))

        self.assertEqual(a.num,b.num)
    
    def test_json_to_file(self):
        obj = 1
        ser = MySerializer.createSerializer('.json')
        with open("test.json", "w+") as output_file:
            ser.dump(obj, output_file)

        with open("test.json", "r+") as f:
            new_obj = ser.load(f)
        
        self.assertEqual(obj, new_obj)

        
class XmlTests(unittest.TestCase):
    def test_xml_primitive(self):
        ser = MySerializer.createSerializer(".xml")
        obj = 1
        self.assertEqual(obj,ser.loads(ser.dumps(obj)))
        obj = True
        self.assertEqual(obj,ser.loads(ser.dumps(obj)))
        obj = "a"
        self.assertEqual(obj,ser.loads(ser.dumps(obj)))
        obj = 1.1
        self.assertEqual(obj,ser.loads(ser.dumps(obj)))
        obj = None
        self.assertEqual(obj,ser.loads(ser.dumps(obj)))

    def test_xml_collections(self):
        ser = MySerializer.createSerializer(".xml")
        obj = [1,2,3,4,5]
        self.assertEqual(obj,ser.loads(ser.dumps(obj)))
        obj = (1,2,3,4,5)
        self.assertEqual(obj,ser.loads(ser.dumps(obj)))
        obj = {1,2,3,4,5}
        self.assertEqual(obj,ser.loads(ser.dumps(obj)))
        obj = {1:1,2:2,3:3,4:4,5:5}
        self.assertEqual(obj,ser.loads(ser.dumps(obj)))

    def test_xml_func(self):        
        ser = MySerializer.createSerializer(".json")
        self.assertEqual(foo(2,2),ser.loads(ser.dumps(foo))(2,2))
        for i,k in zip(gen(1),ser.loads(ser.dumps(gen))(1)):
            self.assertEqual(i,k)  
        self.assertEqual(lam(1),ser.loads(ser.dumps(lam))(1))
        self.assertEqual(first(1),ser.loads(ser.dumps(first))(1))
        self.assertEqual(rec(4),ser.loads(ser.dumps(rec))(4))
        self.assertEqual(firstIn(4),ser.loads(ser.dumps(firstIn))(4))
        

    def test_xml_func_with_lib(self):
        ser = MySerializer.createSerializer(".json")
        self.assertEqual(fooMath(2),ser.loads(ser.dumps(fooMath))(2))

    def test_xml_class(self):
        ser = MySerializer.createSerializer(".xml")
        _class = A
        _serializedClass = ser.loads(ser.dumps(_class))
        a = _class(1)
        b = _serializedClass(1)

        self.assertEqual(a.num,b.num)
        self.assertEqual(a.a_var,b.a_var)
        self.assertEqual(a.a_func(),b.a_func())

    def test_xml_classInheritance(self):
        ser = MySerializer.createSerializer(".xml")
        _class = B
        _serializedClass = ser.loads(ser.dumps(_class))
        a = _class(1)
        b = _serializedClass(1)

        self.assertEqual(a.num,b.num)
        self.assertEqual(a.a_var,b.a_var)
        self.assertEqual(a.a_func(),b.a_func())
        self.assertEqual(a.b_func(),b.b_func())
        
    def test_xml_object(self):
        ser = MySerializer.createSerializer(".xml")
        a = B(1)
        b = ser.loads(ser.dumps(a))
        
        self.assertEqual(a.num,b.num)
        self.assertEqual(a.a_var,b.a_var)

    def test_xml_to_file(self):
        obj = "Pup"
        ser = MySerializer.createSerializer('.xml')
        with open("test.xml", "w+") as output_file:
            ser.dump(obj, output_file)

        with open("test.xml", "r+") as f:
            new_obj = ser.load(f)

        self.assertEqual(obj, new_obj)

unittest.main()